"""게임 서버(Remote MCP, streamable HTTP)용 최소 클라이언트. 표준 라이브러리만 쓴다.

OpenAI가 서버를 직접 부르면 우리 코드가 중간에 끼어들 수 없다(힌트 제한, 정답 검증, 자동 둘러보기).
그래서 게임 서버 호출은 이 클라이언트로 우리가 대신 하고, 결과만 모델에 돌려준다.
"""

import json
import urllib.error
import urllib.request


class McpError(RuntimeError):
    pass


class McpHttp:
    def __init__(self, url: str, timeout: float = 30):
        self.url = url
        self.timeout = timeout
        self.sid: str | None = None
        self._id = 0
        self._ready = False

    # ── 저수준 ──────────────────────────────────────────
    def _post(self, body: dict) -> str:
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.sid:
            headers["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(self.url, json.dumps(body).encode(), headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            self.sid = r.headers.get("Mcp-Session-Id") or self.sid
            return r.read().decode("utf-8")

    @staticmethod
    def _parse(raw: str, ident):
        """JSON 본문 또는 SSE(`data:` 줄)에서 id가 맞는 응답을 찾는다."""
        raw = raw.strip()
        if not raw:
            return None
        chunks = [raw] if raw.startswith("{") else [
            line[5:].strip() for line in raw.splitlines() if line.startswith("data:")
        ]
        for chunk in chunks:
            try:
                msg = json.loads(chunk)
            except ValueError:
                continue
            if ident is None or msg.get("id") == ident:
                return msg
        return None

    def _rpc(self, method: str, params: dict | None = None, notify: bool = False):
        body: dict = {"jsonrpc": "2.0", "method": method}
        ident = None
        if not notify:
            self._id += 1
            ident = self._id
            body["id"] = ident
        if params is not None:
            body["params"] = params
        msg = self._parse(self._post(body), ident)
        if notify:
            return None
        if msg is None:
            raise McpError(f"{method}: 응답이 비어 있습니다.")
        if "error" in msg:
            raise McpError(f"{method}: {msg['error'].get('message', msg['error'])}")
        return msg.get("result", {})

    # ── 공개 ────────────────────────────────────────────
    def connect(self) -> None:
        if self._ready:
            return
        self._rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                 "clientInfo": {"name": "ai-shift-escape", "version": "1"}})
        self._rpc("notifications/initialized", notify=True)
        self._ready = True

    def _reset(self) -> None:
        self.sid, self._ready = None, False

    def list_tools(self) -> list[dict]:
        self.connect()
        return self._rpc("tools/list", {}).get("tools", [])

    def call_tool(self, name: str, arguments: dict) -> str:
        """도구를 호출하고 텍스트 결과를 돌려준다. 세션이 만료됐으면 한 번 다시 연결한다."""
        for attempt in (0, 1):
            try:
                self.connect()
                result = self._rpc("tools/call", {"name": name, "arguments": arguments})
                break
            except urllib.error.HTTPError as exc:
                if attempt == 0 and exc.code in (400, 404):
                    self._reset()
                    continue
                raise McpError(f"게임 서버 HTTP {exc.code}") from exc
        text = "".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")
        return f"[서버 오류] {text}" if result.get("isError") else text
