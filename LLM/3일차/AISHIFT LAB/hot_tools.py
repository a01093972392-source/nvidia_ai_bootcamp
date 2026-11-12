"""my_tools.py 핫 리로드. 파일을 저장하면 재시작 없이 새 도구가 반영된다.

  hot = HotTools(path, to_function_tools, on_swap=..., lock=...)
  await hot.start()            # 처음 한 번 읽는다
  changed = await hot.poll()   # 파일이 바뀌었으면 다시 읽고 True

- 소스를 직접 컴파일해서 실행한다. import/reload를 쓰면 .pyc 캐시(초 단위 mtime) 때문에
  같은 초에 두 번 저장하면 옛 코드가 남을 수 있다.
- 저장 중 문법 오류가 나도 이전 도구를 그대로 쓰고 `error`에 이유를 남긴다. 고치면 자동 복구된다.
- `lock`을 주면 (Game.lock) 진행 중인 턴이 끝난 뒤에 도구를 바꾼다.
"""

import asyncio
import contextlib
import sys
import types
from contextlib import AsyncExitStack
from pathlib import Path


class HotTools:
    def __init__(self, path, to_functions, on_swap=None, lock=None):
        self.path = Path(path)
        self.to_functions = to_functions
        self.on_swap = on_swap
        self.lock = lock
        self.local = None  # 열려 있는 fastmcp Client
        self.functions: list[dict] = []  # OpenAI function tool 목록
        self.names: list[str] = []
        self.revision = 0  # 다시 읽기를 시도할 때마다(성공/실패 모두) 증가
        self.error: str | None = None
        self._sig = None
        self._stack: AsyncExitStack | None = None

    def _signature(self):
        st = self.path.stat()
        return (st.st_mtime_ns, st.st_size)

    def _load_module(self):
        source = self.path.read_text(encoding="utf-8")
        module = types.ModuleType("my_tools")
        module.__file__ = str(self.path)
        previous = sys.modules.get("my_tools")
        sys.modules["my_tools"] = module
        try:
            exec(compile(source, str(self.path), "exec"), module.__dict__)
            if not hasattr(module, "mcp"):
                raise AttributeError("my_tools.py에 `mcp = FastMCP(...)`가 없습니다.")
        except BaseException:
            if previous is not None:
                sys.modules["my_tools"] = previous
            else:
                sys.modules.pop("my_tools", None)
            raise
        return module

    async def _build(self):
        from fastmcp import Client

        module = self._load_module()
        stack = AsyncExitStack()
        try:
            local = await stack.enter_async_context(Client(module.mcp))
            functions = self.to_functions(await local.list_tools())
        except BaseException:
            await stack.aclose()
            raise
        return stack, local, functions

    async def _swap(self, stack, local, functions) -> None:
        async with self.lock or contextlib.nullcontext():
            old = self._stack
            self._stack, self.local, self.functions = stack, local, functions
            self.names = [f["name"] for f in functions]
            if self.on_swap:
                self.on_swap(self)
            if old is not None:
                await old.aclose()

    async def start(self) -> None:
        self._sig = self._signature()
        await self._swap(*await self._build())
        self.revision = 1

    async def poll(self) -> bool:
        """파일이 바뀌었으면 다시 읽는다. 바뀌었으면(성공/실패 모두) True."""
        try:
            sig = self._signature()
        except OSError:
            return False
        if sig == self._sig:
            return False
        self._sig = sig
        await asyncio.sleep(0.15)  # 편집기가 파일을 쓰는 도중을 피한다
        try:
            await self._swap(*await self._build())
            self.error = None
        except Exception as exc:  # 문법 오류 등: 이전 도구를 계속 쓴다
            self.error = f"{type(exc).__name__}: {exc}"
        self.revision += 1
        return True

    async def close(self) -> None:
        if self._stack is not None:
            await self._stack.aclose()
            self._stack = None
