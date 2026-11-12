"""입출력 없는 게임 루프. 웹 서버와 터미널(client.py)이 함께 쓴다.

say(text)는 이벤트(dict) 목록을 돌려준다.
  {"kind": "call",  "name", "args"}                   AI가 고른 도구 호출
  {"kind": "game",  "text", "scene", [title, objects, exits]}  게임 서버 화면
  {"kind": "door",  "id", "label", "move"}            문이 열렸다 (move=True면 장소가 바뀐다)
  {"kind": "tool",  "text"}                           내 도구(my_tools) 결과
  {"kind": "ai",    "text", [guarded]}                AI의 짧은 안내
  {"kind": "guard", "text"}                           규칙에 따라 막았다 (힌트 요청 없음, 도구 없는 정답 등)

게임 서버 호출은 모두 여기를 지난다 (OpenAI가 직접 부르지 않는다):
  - 힌트: 사용자가 요청한 턴에만 실행
  - 정답 제출: 사용자가 준 값 / 내 도구가 계산한 값 / 화면에 적힌 값일 때만
  - 문을 열거나 이동하면 observe를 자동으로 불러 새 장소를 바로 보여준다
"""

import asyncio
import json

import guards
from ui import detect_theme, parse_location


def format_args(args: dict) -> str:
    return ", ".join(f"{k}={v}" for k, v in args.items() if k != "session_id" and v is not None)


class Game:
    def __init__(self, openai, local, tools, rules, model, server=None):
        self.openai = openai
        self.local = local  # fastmcp Client(my_tools), 이미 열려 있어야 한다
        self.my_tools = list(tools)  # my_tools.py의 함수 도구 (OpenAI function tool 형식)
        self.server = server  # game_server.GameServer (없으면 게임 도구 없이 동작)
        self.rules = rules
        self.model = model
        self.pending: list[dict] = []
        self.last_id = None
        self.scene: str | None = None
        self.lock = asyncio.Lock()
        # 검문에 쓰는 기억
        self.user_texts: list[str] = []
        self.tool_outputs: list[str] = []  # 내 도구가 계산한 값들
        self.game_texts: list[str] = []  # 화면에 보인 글
        self.turn_text = ""
        self.place: str | None = None
        self.exit_labels: dict[str, str] = {}
        self._last_loc: dict | None = None

    # ── 도구 목록 ───────────────────────────────────────
    @property
    def tools(self) -> list[dict]:
        return (list(self.server.function_tools) if self.server else []) + self.my_tools

    def swap_tools(self, local, tools) -> None:
        """my_tools.py가 바뀌었을 때 호출한다. 진행 중인 턴이 없을 때(lock 안에서) 쓴다."""
        self.local, self.my_tools = local, list(tools)

    async def _create(self, **kw):
        call = lambda: asyncio.to_thread(  # noqa: E731
            self.openai.responses.create,
            model=self.model,
            instructions=self.rules,
            tools=self.tools,
            **kw,
        )
        try:
            return await call()
        except Exception as exc:
            # 직전 응답의 도구 호출이 답을 못 받은 채 남은 꼬인 상태면, 대화 연결을 끊고 한 번 다시 시도한다.
            if "No tool output found" in str(exc) and kw.get("previous_response_id"):
                self.last_id = None
                kw["previous_response_id"] = None
                kw["input"] = [m for m in kw["input"] if m.get("type") != "function_call_output"]
                return await call()
            raise

    async def say(self, said: str) -> list[dict]:
        async with self.lock:
            return await self._say(said)

    # ── 한 턴 ───────────────────────────────────────────
    async def _say(self, said: str) -> list[dict]:
        events: list[dict] = []
        self.user_texts.append(said)
        self.turn_text = said
        self.pending.append({"role": "user", "content": said})
        response = await self._create(
            input=self.pending,
            previous_response_id=self.last_id,
            parallel_tool_calls=False,  # 한 턴에 도구는 하나만. 그래야 흐름을 따라갈 수 있다.
        )
        self.last_id = response.id
        self.pending = []

        used_my_tool = False
        for item in response.output:
            if item.type != "function_call":
                continue
            try:
                args = json.loads(item.arguments or "{}")
            except ValueError:
                args = {}
            if self.server and item.name in self.server.names:
                output = await self._game_call(item.name, args, events)
                self.pending.append({"type": "function_call_output", "call_id": item.call_id, "output": output})
            else:
                used_my_tool = True
                output = await self._my_tool_call(item.name, args, events)
                self.pending.append({"type": "function_call_output", "call_id": item.call_id, "output": output})

        if used_my_tool:
            # 내 도구 결과를 AI에게 돌려주고 설명만 받는다. 여기서 도구를 또 부르지 못하게 막는다.
            follow_up = await self._create(
                input=self.pending, previous_response_id=self.last_id, tool_choice="none")
            self.last_id = follow_up.id
            self.pending = []
            if follow_up.output_text:
                events.append({"kind": "ai", "text": follow_up.output_text})
        elif response.output_text:
            events.append(self._checked_ai_text(response.output_text))
        return events

    def _checked_ai_text(self, text: str) -> dict:
        """계산·해독을 요청받았는데 도구를 한 번도 부르지 않았다면 AI가 만든 답은 쓰지 않는다."""
        if guards.needs_tool(self.turn_text):
            names = [t["name"] for t in self.my_tools]
            return {"kind": "ai", "guarded": True,
                    "text": guards.REFUSAL_HAS_TOOL if names else guards.REFUSAL_NO_TOOL}
        return {"kind": "ai", "text": text}

    # ── 내 도구 ─────────────────────────────────────────
    async def _my_tool_call(self, name: str, args: dict, events: list[dict]) -> str:
        events.append({"kind": "call", "name": name, "args": format_args(args)})
        try:
            result = await self.local.call_tool(name, args)
            output = result.content[0].text
        except Exception as exc:
            # 결과를 돌려주지 못하면 이후 모든 턴이 "No tool output found"로 막힌다.
            output = f"[도구 오류] {type(exc).__name__}: {exc}"
        self.tool_outputs.append(output)
        events.append({"kind": "tool", "text": output})
        return output

    # ── 게임 서버 ───────────────────────────────────────
    def _answer_ok(self, answer: str) -> bool:
        return guards.appears(answer, self.user_texts + self.tool_outputs + self.game_texts)

    def _show(self, text: str, events: list[dict]) -> dict | None:
        """게임 화면 이벤트를 추가하고 장소 정보를 돌려준다."""
        self.game_texts.append(text)
        self.scene = detect_theme(text, self.scene)
        event = {"kind": "game", "text": text, "scene": self.scene}
        loc = parse_location(text)
        if loc:  # observe 결과: 장소 이름, 오브젝트, 출구
            event.update(loc)
        events.append(event)
        return loc

    async def _game_call(self, name: str, args: dict, events: list[dict]) -> str:
        events.append({"kind": "call", "name": name, "args": format_args(args)})
        action, target = args.get("action"), str(args.get("target") or "")

        if name == "interact" and action == "hint" and not guards.hint_requested(self.turn_text):
            events.append({"kind": "guard", "text": guards.HINT_BLOCKED_TO_USER})
            return guards.HINT_BLOCKED_TO_MODEL
        if name == "submit_answer" and not self._answer_ok(str(args.get("answer", ""))):
            events.append({"kind": "guard", "text": guards.ANSWER_BLOCKED_TO_USER})
            return guards.ANSWER_BLOCKED_TO_MODEL

        prev_place, was_exit = self.place, target in self.exit_labels
        try:
            out = await self.server.call(name, args)
        except Exception as exc:
            events.append({"kind": "guard", "text": f"⚠ 게임 서버 호출에 실패했습니다. {exc}"})
            return f"[서버 오류] {type(exc).__name__}: {exc}"
        loc = self._show(out, events)
        if loc:
            self._remember(loc)

        if name == "start_game" and not out.startswith("[서버 오류]"):
            # 새 게임: 이전 판의 장소·화면 기억을 지우고, 시작 장소를 바로 보여준다 (둘러보기를 말하지 않아도)
            self.place, self.exit_labels, self._last_loc = None, {}, None
            self.game_texts = [out]
            text, _ = await self._auto_look(None, "", events, label="자동 · 시작 위치")
            return out + text

        auto_text = ""
        # 행동이 성공했으면 장소를 다시 읽어 화면을 맞춘다 (이동, 새로 생긴 문/물체). 바뀐 게 없으면 조용히 넘어간다.
        refresh = (name == "interact" and action != "hint") or name == "submit_answer"
        if refresh and not guards.failed(out) and self.scene != "escape":
            changed = False
            if loc:  # 응답에 이미 새 장소 박스가 들어 있다
                changed = bool(prev_place) and loc["title"] != prev_place
                if changed:
                    events.insert(len(events) - 1, self._door_event(target, True))  # 화면보다 먼저
            else:
                auto_text, changed = await self._auto_look(prev_place, target, events)
            opened = any(e["kind"] == "door" and e.get("id") == target for e in events)
            if name == "interact" and not changed and not opened and guards.succeeded(out) and guards.doorish(target):
                events.append(self._door_event(target, False))  # 장소는 그대로, 문만 열렸다
        return out + auto_text

    def _door_event(self, target: str, move: bool) -> dict:
        return {"kind": "door", "id": target, "label": self.exit_labels.get(target, ""), "move": move}

    async def _auto_look(self, prev_place, target, events, label="자동 · 이동 확인") -> tuple[str, bool]:
        """문을 열거나 이동한 직후 observe를 자동으로 불러 새 장소를 바로 보여준다. (모델에게 줄 글, 장소가 바뀌었나)"""
        try:
            obs = await self.server.call("observe", {})
        except Exception:
            return "", False
        loc = parse_location(obs)
        if not loc:
            return "", False
        changed = bool(prev_place) and loc["title"] != prev_place
        sig = lambda x: json.dumps([x["objects"], x["exits"]], ensure_ascii=False)  # noqa: E731
        shown = changed or self._last_loc is None or sig(loc) != sig(self._last_loc)
        if changed:
            events.append(self._door_event(target, True))  # 문이 열린 다음 새 장면이 나온다
        if shown:
            old_exits = {e["id"] for e in (self._last_loc or {"exits": []})["exits"]}
            events.append({"kind": "call", "name": "observe", "args": label})
            self._show(obs, events)
            if not changed and self._last_loc is not None:  # 같은 장소에 새 문이 생겼다 → 열리며 나타난다
                for e in loc["exits"]:
                    if e["id"] not in old_exits:
                        events.append({"kind": "door", "id": e["id"], "label": e["label"],
                                       "move": False, "appeared": True})
        self._remember(loc)
        # 바뀐 게 없으면 모델에게도 같은 화면을 또 주지 않는다
        return (f"\n\n[자동 둘러보기]\n{obs}" if shown else ""), changed

    def _remember(self, loc: dict) -> None:
        self.place = loc["title"]
        self.exit_labels = {e["id"]: e["label"] for e in loc["exits"]}
        self._last_loc = loc
