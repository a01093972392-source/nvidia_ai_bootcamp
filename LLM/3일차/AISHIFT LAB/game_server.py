"""게임 서버 도구를 모델에게 '함수 도구'로 보여주고, 호출은 우리가 대신 실행한다.

- session_id는 모델에게 숨긴다. start_game 응답에서 우리가 받아 두었다가 호출마다 자동으로 붙인다.
  (모델이 세션 값을 베껴 쓰다 틀리는 일이 없어진다)
"""

import asyncio
import re

HIDDEN = "session_id"


def to_function_tool(tool: dict) -> dict:
    schema = dict(tool.get("inputSchema") or {"type": "object", "properties": {}})
    props = {k: v for k, v in (schema.get("properties") or {}).items() if k != HIDDEN}
    schema["properties"] = props
    schema["required"] = [r for r in schema.get("required", []) if r != HIDDEN]
    desc = (tool.get("description") or "").strip()
    return {"type": "function", "name": tool["name"], "description": desc, "parameters": schema}


class GameServer:
    def __init__(self, mcp):
        self.mcp = mcp
        self.session_id: str | None = None
        self.function_tools: list[dict] = []
        self.names: set[str] = set()
        self._needs_session: set[str] = set()

    async def load(self) -> None:
        raw = await asyncio.to_thread(self.mcp.list_tools)
        self.function_tools = [to_function_tool(t) for t in raw]
        self.names = {t["name"] for t in raw}
        self._needs_session = {
            t["name"] for t in raw if HIDDEN in ((t.get("inputSchema") or {}).get("properties") or {})
        }

    async def call(self, name: str, args: dict) -> str:
        args = {k: v for k, v in args.items() if k != HIDDEN}
        if name in self._needs_session:
            if not self.session_id:
                return "[서버 오류] 게임이 아직 시작되지 않았습니다. 먼저 start_game을 호출하세요."
            args[HIDDEN] = self.session_id
        out = await asyncio.to_thread(self.mcp.call_tool, name, args)
        if name == "start_game":
            m = re.search(r"session_id:\s*(\S+)", out)
            if m:
                self.session_id = m.group(1)
        return out
