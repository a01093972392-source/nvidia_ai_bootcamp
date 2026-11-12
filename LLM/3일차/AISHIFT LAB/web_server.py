"""웹 방탈출 서버. 실행: python web_server.py  →  http://127.0.0.1:8765

외부 패키지 없이 표준 라이브러리 HTTP 서버를 쓴다. 게임 루프(engine.Game)는
백그라운드 asyncio 루프에서 돌고, my_tools.py는 client.py와 똑같이 fastmcp 도구로 호출된다.
"""

import asyncio
import json
import os
import re
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

WEB_DIR = Path(__file__).with_name("web")
PORT = int(os.environ.get("PORT", "8765"))


class Runner:
    """Game을 별도 스레드의 asyncio 루프에 올리고 동기 인터페이스로 감싼다."""

    def __init__(self) -> None:
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()
        self.game = None
        self.hot = None
        self.error: str | None = None

    def start(self) -> None:
        asyncio.run_coroutine_threadsafe(self._init(), self.loop).result(timeout=60)

    async def _init(self) -> None:
        try:
            from dotenv import load_dotenv
            from openai import OpenAI

            import client  # RULES, GAME_URL 등 설정 재사용 (main은 실행되지 않는다)
            from engine import Game
            from game_server import GameServer
            from hot_tools import HotTools
            from mcp_http import McpHttp

            load_dotenv(Path(__file__).with_name(".env"))
            if not os.environ.get("OPENAI_API_KEY"):
                self.error = "OPENAI_API_KEY가 없습니다. .env를 확인하세요."
                return
            server = GameServer(McpHttp(client.GAME_URL))
            await server.load()  # 게임 서버 도구 목록 (연결 실패는 여기서 error로 보인다)
            hot = HotTools(client.MY_TOOLS_PATH, client.to_function_tools)
            await hot.start()  # my_tools.py 문법 오류면 여기서 error로 보인다
            self.game = Game(OpenAI(), hot.local, hot.functions, client.RULES, client.MODEL, server)
            # 이후 변경은 진행 중인 턴이 끝난 뒤(game.lock) 반영된다.
            hot.lock = self.game.lock
            hot.on_swap = lambda h: self.game.swap_tools(h.local, h.functions)
            self.hot = hot
            asyncio.ensure_future(self._watch())
        except Exception as exc:  # 설치/설정 문제를 브라우저에 보여준다
            self.error = f"{type(exc).__name__}: {exc}"

    async def _watch(self) -> None:
        while True:
            await asyncio.sleep(0.7)
            try:
                await self.hot.poll()
            except Exception as exc:  # 감시가 죽지 않게 한다
                self.hot.error = f"{type(exc).__name__}: {exc}"

    def info(self) -> dict:
        hot = self.hot
        return {
            "ready": self.game is not None,
            "tools": hot.names if hot else [],
            "error": self.error,
            "revision": hot.revision if hot else 0,  # my_tools.py를 다시 읽을 때마다 증가
            "reload_error": hot.error if hot else None,  # 문법 오류 등 (이전 도구는 유지)
        }

    def say(self, text: str) -> list[dict]:
        if self.game is None:
            raise RuntimeError(self.error or "게임이 아직 준비되지 않았습니다.")
        fut = asyncio.run_coroutine_threadsafe(self.game.say(text), self.loop)
        return fut.result(timeout=180)


def make_handler(runner):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):  # 조용히
            pass

        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, code: int, data) -> None:
            self._send(code, json.dumps(data, ensure_ascii=False).encode(), "application/json; charset=utf-8")

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                self._send(200, (WEB_DIR / "index.html").read_bytes(), "text/html; charset=utf-8")
            elif re.fullmatch(r"/[\w.-]+\.(js|css)", self.path) and (WEB_DIR / self.path[1:]).is_file():
                kind = "javascript" if self.path.endswith(".js") else "css"
                self._send(200, (WEB_DIR / self.path[1:]).read_bytes(), f"text/{kind}; charset=utf-8")
            elif self.path == "/favicon.ico":
                self._send(204, b"", "image/x-icon")
            elif self.path == "/api/state":
                self._json(200, runner.info())
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self):
            if self.path != "/api/say":
                return self._send(404, b"not found", "text/plain")
            try:
                length = int(self.headers.get("Content-Length", "0"))
                text = json.loads(self.rfile.read(length) or b"{}").get("text", "").strip()
                if not text:
                    return self._json(400, {"error": "빈 입력입니다."})
                self._json(200, {"events": runner.say(text)})
            except Exception as exc:
                self._json(500, {"error": f"{type(exc).__name__}: {exc}"})

    return Handler


def make_server(runner, port: int = PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), make_handler(runner))


if __name__ == "__main__":
    runner = Runner()
    runner.start()
    server = make_server(runner)
    url = f"http://127.0.0.1:{PORT}"
    print(f"AI SHIFT LAB 웹 방탈출: {url}")
    if runner.error:
        print(f"[경고] {runner.error}")
    if not os.environ.get("NO_BROWSER"):
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
