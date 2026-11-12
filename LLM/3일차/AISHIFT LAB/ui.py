"""장소(장면)별 터미널 UI. client.py가 불러 쓴다. 학생은 고치지 않아도 된다.

게임 서버는 observe 결과를 아래처럼 장소 이름 헤더가 있는 박스로 돌려준다.

    ┌────
    │  AI 연구실
    ├────
    │  research_pc        연구용 PC
    │  나가는 곳
    │  server_room_door   서버실 출입문

이 헤더에서 현재 장소를 읽는다. 새 장소를 꾸미려면 THEMES와 PLACES에 항목을 추가한다.
`python ui.py` 로 API 키 없이 테마를 미리 볼 수 있다.
"""

import os
import re
from dataclasses import dataclass

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.text import Text

    RICH = True
except ImportError:  # rich가 없으면 기존 print 출력으로 되돌린다.
    RICH = False


@dataclass(frozen=True)
class Theme:
    title: str
    color: str
    mood: str
    art: str


THEMES: dict[str, Theme] = {
    "intro": Theme(
        "AI SHIFT LAB",
        "cyan",
        "비상 전원 복구. 깜빡거리는 모니터 앞에서 눈을 뜬다...",
        r"""
    ╔═══════════════════════════╗
    ║   A I   S H I F T   L A B ║
    ║      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ║
    ║        E S C A P E        ║
    ╚═══════════════════════════╝""",
    ),
    "lab": Theme(
        "AI 연구실",
        "green",
        "오래전에 폐쇄된 연구실. 책상, 낡은 PC, 잠긴 보관함이 보인다.",
        r"""
     ┌──────────────┐   ┌────┐
     │ > _ ▌▌▌ 0101 │   │ ▒▒ │ 보관함
     └──────┬┬──────┘   └────┘
       ═════╧╧═════ 책상        [서버실]""",
    ),
    "server": Theme(
        "서버실",
        "magenta",
        "꺼진 서버 랙들 사이로 비상등만 붉게 깜빡인다.",
        r"""
     ▐█▌ ▐█▌ ▐█▌ ▐█▌ ▐█▌
     ▐▒▌ ▐▒▌ ▐▒▌ ▐▒▌ ▐▒▌
     ▐░▌ ▐░▌ ▐░▌ ▐░▌ ▐░▌   ● ● ●""",
    ),
    "control": Theme(
        "보안 통제실",
        "red",
        "벽을 가득 채운 모니터에 연구소 곳곳의 영상이 흐른다.",
        r"""
     ┌────┐┌────┐┌────┐
     │░▒░ ││ ▒▒ ││░░▒ │  [CCTV]
     └────┘└────┘└────┘
       ═══════ 콘솔 ═══════""",
    ),
    "room": Theme(
        "연구소",
        "blue",
        "복도의 조명은 꺼져 있다.",
        r"""
     |‾‾|  |‾‾|  |‾‾|
     |__|  |__|  |__|""",
    ),
    "escape": Theme(
        "탈 출 성 공",
        "bright_green",
        "잠겨 있던 외부 출입문이 열린다. 바깥 공기다!",
        r"""
      \ | /
     -- ★ --   EXIT
      / | \
    ┌───────┐
    │  ▒▒▒  │ ←
    └───────┘""",
    ),
}

# 헤더의 장소 이름에 이 낱말이 들어 있으면 해당 테마를 쓴다. 없으면 "room"에 이름만 붙인다.
PLACES: list[tuple[str, str]] = [
    ("연구실", "lab"),
    ("서버실", "server"),
    ("통제실", "control"),
    ("관제", "control"),
]
ESCAPE_WORDS = ("탈출에 성공", "탈출 성공", "축하합니다", "클리어", "THE END")
INTRO_WORDS = ("눈을 떠보니", "[SYSTEM]", "비상 전원")

# id는 영문/숫자로 시작하고 _ . - 를 쓸 수 있다. id와 라벨 사이는 공백 1칸 이상(탭 포함).
_ID_LINE = re.compile(r"^│\s+([A-Za-z0-9][A-Za-z0-9_.\-]*)\s+(\S.*?)\s*$")
_EXIT_HEAD = re.compile(r"^(나가는\s*곳|나갈\s*수\s*있는\s*곳|출구|출입구|이동(\s*(가능|할\s*수\s*있는))?\s*곳?|exits?)", re.I)


def parse_location(text: str) -> dict | None:
    """observe 박스에서 장소 이름, 오브젝트, 출구를 뽑는다. 박스가 아니면 None.

    읽지 못한 줄은 `unparsed`에 담아 돌려준다 (조용히 버리지 않는다 — 화면에서 확인할 수 있게)."""
    lines = text.strip().splitlines()
    if not lines or not lines[0].startswith("┌"):
        return None
    title = None
    objects: list[dict] = []
    exits: list[dict] = []
    unparsed: list[str] = []
    in_exits = False
    for line in lines[1:]:
        line = line.strip()
        if line.startswith("├") or line.startswith("└"):
            continue
        body = line.lstrip("│").strip()
        if title is None and line.startswith("│"):
            title = body or None
            continue
        if not body:
            continue
        m = _ID_LINE.match(line)
        if m:
            (exits if in_exits else objects).append({"id": m.group(1), "label": m.group(2)})
        elif _EXIT_HEAD.match(body):
            in_exits = True  # '나가는 곳' 같은 제목: 아래 줄은 출구
        else:
            in_exits = False  # 다른 제목: 아래 줄은 다시 일반 오브젝트
            if len(body) > 18 or re.search(r"[.!?。]", body):  # 제목이 아니라 읽지 못한 문장으로 본다
                unparsed.append(body)
    if title is None:
        return None
    return {"title": title, "objects": objects, "exits": exits, "unparsed": unparsed}


def detect_theme(text: str, previous: str | None) -> str:
    """서버 응답에서 현재 장면을 정한다. 장소 헤더 → 탈출 → 오프닝 순, 못 찾으면 직전 장면."""
    if any(w in text for w in ESCAPE_WORDS):
        return "escape"
    loc = parse_location(text)
    if loc:
        for word, key in PLACES:
            if word in loc["title"]:
                return key
        return "room"
    if any(w in text for w in INTRO_WORDS):
        return "intro"
    return previous or "intro"


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?。])\s+|\n", text)
    return [p.strip() for p in parts if p.strip()]


class UI:
    def __init__(self) -> None:
        self.rich = RICH and not os.environ.get("NO_RICH")
        self.console = Console() if self.rich else None
        self.current: str | None = None
        self.place: str | None = None  # 마지막으로 본 장소 이름 (room 테마 제목)

    def _title(self, key: str) -> str:
        return self.place if key == "room" and self.place else THEMES[key].title

    # ── 장면 전환 ───────────────────────────────────────
    def enter(self, key: str) -> None:
        if key == self.current:
            return
        self.current = key
        theme = THEMES[key]
        title = self._title(key)
        if not self.rich:
            print(f"\n=== {title} ===\n{theme.mood}")
            return
        self.console.print()
        self.console.print(Rule(f"[bold {theme.color}]{title}[/]", style=theme.color))
        self.console.print(Text(theme.art, style=theme.color))
        self.console.print(Text(theme.mood, style=f"italic {theme.color}"), justify="center")

    # ── 출력 ────────────────────────────────────────────
    def banner(self) -> None:
        self.enter("intro")

    def info(self, message: str) -> None:
        if self.rich:
            self.console.print(f"[dim]{message}[/]")
        else:
            print(message)

    def call(self, name: str, shown: str) -> None:
        if self.rich:
            self.console.print(f"\n[dim]⚙ [실행] {name}({shown})[/]")
        else:
            print(f"\n[실행] {name}({shown})")

    def game(self, text: str) -> None:
        """게임 서버 화면. 장소를 읽어 테마 패널로 보여준다."""
        loc = parse_location(text)
        if loc:
            self.place = loc["title"]
        key = detect_theme(text, self.current)
        self.enter(key)
        theme = THEMES[key]
        if not self.rich:
            print(f"\n{text}")
            return
        self.console.print(Panel(Text(text, style=theme.color),
                                 title=f"[bold]{self._title(key)}[/]",
                                 border_style=theme.color, padding=(1, 2)))
        if key == "escape":
            self.console.print(Text("★ ☆ ★  CONGRATULATIONS  ★ ☆ ★", style="bold bright_green"),
                               justify="center")

    def guard(self, text: str) -> None:
        """규칙에 따라 막은 것(힌트 요청 없음, 도구 없이 만든 답 등)."""
        if self.rich:
            self.console.print(Panel(text, border_style="yellow", padding=(0, 2)))
        else:
            print(f"\n{text}")

    def door(self, label: str, move: bool = False) -> None:
        """문이 열리는 연출 (터미널): 닫힌 문이 가운데부터 갈라진다."""
        name = f" {label}" if label else ""
        if not self.rich or os.environ.get("NO_ANIM") or not self.console.is_terminal:
            print(f"\n🚪 문이 열립니다.{name}")
            return
        import time

        for gap in range(0, 9, 2):
            left, right = "█" * (10 - gap), "█" * (10 - gap)
            self.console.print(f"\r  [bold yellow]▐{left}[/]{' ' * (gap * 2)}[bold yellow]{right}▌[/]  🚪{name}", end="")
            time.sleep(0.09)
        self.console.print()

    def tool(self, text: str) -> None:
        if self.rich:
            self.console.print(Panel(text, title="🔧 내 도구 결과", border_style="magenta"))
        else:
            print(f"\n{text}")

    def ai(self, text: str) -> None:
        if self.rich:
            self.console.print(f"\n[bold cyan][AI][/] {text}")
        else:
            print(f"\n[AI] {text}")

    def prompt(self) -> str:
        if self.rich:
            theme = THEMES[self.current or "intro"]
            return self.console.input(f"\n[bold {theme.color}]>[/] ").strip()
        return input("\n> ").strip()


if __name__ == "__main__":
    ui = UI()
    ui.banner()
    samples = [
        "[SYSTEM] 비상 전원 — 복구 완료\n\n눈을 떠보니 깜빡거리는 모니터가 보입니다.",
        "┌────\n│  AI 연구실\n├────\n│\n│  research_pc        연구용 PC\n│\n│  나가는 곳\n│  server_room_door   서버실 출입문\n└────",
        "┌────\n│  서버실\n├────\n│  rack_a   서버 랙 A\n└────",
        "축하합니다! 탈출에 성공했습니다.",
    ]
    for s in samples:
        ui.game(s)
