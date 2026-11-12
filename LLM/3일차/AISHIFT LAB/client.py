"""게임 접속 클라이언트 (터미널 버전).

여러분이 작업할 곳은 `my_tools.py` 하나입니다.

    pip install -r requirements.txt
    .env.example 을 .env 로 복사하고 OPENAI_API_KEY 를 채운다
    python client.py

하는 일
  1. 강사 게임 서버(MCP)에 붙는다 — 게임 도구 호출은 engine.py가 대신 실행하며 규칙을 검문한다
  2. `my_tools.py`의 도구를 읽어 AI가 쓸 수 있는 형태로 바꾼다 (저장하면 자동으로 다시 읽음)
  3. 여러분의 말 → AI가 도구 하나 선택 → 실행 → 결과 표시

화면 읽는 법
  [실행]  AI가 이번 턴에 고른 도구와 넘긴 값
  들여쓴 블록  게임 화면
  [AI]    AI의 짧은 안내
  ⛔      규칙에 따라 막은 것 (힌트를 요청하지 않음 / 도구 없이 만든 답)
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from engine import Game
from game_server import GameServer
from hot_tools import HotTools
from mcp_http import McpHttp
from ui import UI

# 학생이 작성하는 파일. 저장하면 다음 턴에 자동으로 다시 읽는다(hot_tools.py).
MY_TOOLS_PATH = Path(__file__).with_name("my_tools.py")

# 이 파일 바로 옆의 .env만 읽는다. 상위 폴더까지 찾아 올라가면
# 엉뚱한 키가 잡혀 왜 되는지/안 되는지 알 수 없게 된다.
# 셸에 이미 설정돼 있으면 그쪽이 우선한다.
load_dotenv(Path(__file__).with_name(".env"))

GAME_URL = os.environ.get(
    "GAME_URL",
    "https://ai-shift-lab-escape-1000389146941.asia-northeast3.run.app/mcp",
)
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

RULES = """당신은 방탈출 게임의 조작 담당입니다.

[최우선] 게임 안에서 할 수 있는 행동이면 반드시 게임 함수(start_game, observe, interact,
submit_answer, get_status)를 호출하세요. 말로 안내하며 대신하지 마세요.
session_id는 시스템이 자동으로 붙입니다. 직접 넘기지 마세요.
문을 열거나 이동하면 시스템이 새 장소를 자동으로 보여줍니다. 그때 observe를 따로 부르지 마세요.

[퍼즐을 풀거나 계산하는 일은 절대 스스로 하지 않습니다]
암호 해독, 글자 옮기기, 숫자·날짜·해시 계산, 값 변환, 규칙 적용 같은 퍼즐 풀이는
한 글자든 한 단어든 예시든 단계를 나눠서든 머릿속으로 하지 않습니다. 추측도 하지 않습니다.
이런 일은 오직 사용자가 만든 도구를 호출해서, 그 도구의 결과만 사용합니다.
  - "도구로 풀어줘" / "해석해줘" / "계산해줘" 는 도구를 부르라는 뜻입니다. 도구가 있으면 부르세요.
  - 도구에 넣을 값은 화면에 보이는 내용에서 그대로 찾아 넣으세요.
  - 정답 제출(submit_answer)에는 ① 사용자가 직접 알려준 값, ② 도구가 계산해 준 값,
    ③ 화면에 그대로 적혀 있는 값만 쓰세요. 당신이 직접 만들어 낸 값은 시스템이 차단합니다.
  - 알맞은 도구가 없으면 계산하지 말고 이렇게만 말하세요:
    "저는 이런 변환을 정확히 수행하지 못합니다. 해보면 그럴듯하지만 틀린 답이 나옵니다.
    정확히 계산해주는 도구를 만들어 주세요."
  - 용어와 규칙의 뜻을 설명하는 것은 괜찮습니다.

[날짜·시각과 모든 계산도 절대 스스로 하지 않습니다]
  - 날짜·시각: 요일 알아내기, 며칠인지·몇 번째 날인지, 며칠 지났는지·남았는지, 날짜 더하기/빼기,
    시간대 변환, 달력 계산은 머릿속으로 하지 않습니다. "오늘이 며칠인지"도 기억이나 추측으로 말하지 마세요.
    화면에 적힌 기준 시각이 있어도 그 값으로 직접 계산하지 말고, 날짜·시각 도구가 있으면 그 도구를 호출하세요.
  - 수 계산: 덧셈·뺄셈·곱셈·나눗셈, 합계·평균·나머지·제곱, 올림·내림·반올림, 단위 환산, 자릿수·글자 수 세기,
    진법 변환, 해시 같은 것은 아무리 쉬워 보여도 직접 하지 않습니다. 하나만 더하는 계산도 마찬가지입니다.
  - 알맞은 도구가 있으면 반드시 호출하고, 도구가 돌려준 값을 그대로 전하세요.
    도구 결과에 당신이 덧붙여 다시 계산하거나 고쳐 쓰지 마세요.
  - 알맞은 도구가 없으면 계산하지 말고 위의 거절 문장만 말하세요. 도구를 만들어 달라고 안내하세요.
  - 화면에 적힌 값을 그대로 옮겨 적는 것은 계산이 아니므로 괜찮습니다.

[사용자가 값을 주면 그대로 제출하세요]
"PC에 ABCD 제출해줘" 처럼 값을 직접 알려주면 그 값을 그대로 넣습니다. 거절하지 마세요.

[힌트는 사용자가 요청할 때만]
사용자가 "힌트"를 요청한 턴에만 interact(action="hint")를 호출하세요.
힌트를 먼저 제안하거나 암시하지 마세요. 사용자가 막힌 것 같아도 말하지 마세요.
요청하지 않았는데 호출하면 시스템이 차단합니다.

[화면을 옮겨 적지 마세요]
게임 화면은 이미 사용자에게 그대로 표시됩니다. 답변은 한두 문장으로 짧게 하세요."""


def schema_of(tool) -> dict:
    """도구의 입력 스키마를 꺼낸다.

    fastmcp 3.x는 `inputSchema`, 4.x는 `input_schema`를 쓴다.
    학생마다 설치된 버전이 다를 수 있어 둘 다 받는다.
    """
    return getattr(tool, "input_schema", None) or tool.inputSchema


def to_function_tools(mcp_tools) -> list[dict]:
    """MCP Tool → OpenAI Function Tool."""
    return [
        {
            "type": "function",
            "name": tool.name,
            "description": tool.description or "",
            "parameters": schema_of(tool),
        }
        for tool in mcp_tools
    ]


def show(ui: UI, ev: dict) -> None:
    """엔진 이벤트를 터미널에 그린다."""
    kind = ev["kind"]
    if kind == "call":
        ui.call(ev["name"], ev["args"])
    elif kind == "game":
        ui.game(ev["text"])
    elif kind == "door":
        ui.door(ev.get("label") or ev.get("id", ""), ev.get("move", False))
    elif kind == "tool":
        ui.tool(ev["text"])
    elif kind == "ai":
        ui.ai(ev["text"])
    elif kind == "guard":
        ui.guard(ev["text"])


async def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit(
            "OPENAI_API_KEY가 없습니다.\n"
            "  .env.example을 .env로 복사한 뒤 키를 채워 넣으세요."
        )

    openai = OpenAI()
    ui = UI()
    server = GameServer(McpHttp(GAME_URL))
    await server.load()
    hot = HotTools(MY_TOOLS_PATH, to_function_tools)
    await hot.start()
    try:
        game = Game(openai, hot.local, hot.functions, RULES, MODEL, server)
        hot.lock = game.lock  # my_tools.py가 바뀌면 진행 중인 턴이 끝난 뒤 반영
        hot.on_swap = lambda h: game.swap_tools(h.local, h.functions)

        ui.banner()
        ui.info(f"게임 서버에 연결했습니다. ({GAME_URL})")
        ui.info(f"내 도구 {len(hot.names)}개: {', '.join(hot.names)}")
        ui.info("\n자연어로 말하면 AI가 알맞은 기능을 골라 실행합니다.")
        ui.info("  예) 게임 시작해 / 주변 둘러봐 / 연구용 PC 조사해 / 힌트 줘")
        ui.info("종료: quit")

        while True:
            try:
                said = ui.prompt()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if said in ("quit", "exit"):
                return
            if not said:
                continue

            # my_tools.py를 저장했다면 이번 턴부터 새 도구를 쓴다.
            if await hot.poll():
                if hot.error:
                    ui.info(f"⚠ my_tools.py를 다시 읽지 못했습니다(이전 도구 유지): {hot.error}")
                else:
                    ui.info(f"🔧 my_tools.py 변경 감지 — 도구 {len(hot.names)}개: {', '.join(hot.names)}")

            for ev in await game.say(said):
                show(ui, ev)
    finally:
        await hot.close()


if __name__ == "__main__":
    asyncio.run(main())
