"""AI가 지켜야 하는 규칙을 '부탁'이 아니라 코드로 강제하는 검문 규칙.

1. 퍼즐 해독·계산·변환은 도구 없이 AI가 스스로 하지 않는다.
   - 정답 제출(submit_answer)의 값은 사용자가 말했거나, 내 도구가 계산했거나, 화면에 적혀 있어야 한다.
   - 계산·해독 요청인데 도구를 한 번도 부르지 않고 낸 AI의 답은 쓰지 않는다.
2. 힌트는 사용자가 요청할 때만 준다.
3. 문을 열거나 이동했는지 판단한다 (자동 둘러보기, 문 열림 연출에 쓴다).
"""

import re

HINT_RE = re.compile(r"힌트|hint|막혔|막혀|도와|도움", re.I)
NEED_TOOL_RE = re.compile(
    r"해석|해독|복호|풀어|계산|변환|디코|암호|구해|몇\s*번째|해시|더해|옮겨|시프트|세어|"
    # 날짜·시각: 요일, 며칠, 몇 월/년, 일수, 달력, 기준 시각, 디데이
    r"날짜|요일|며칠|몇\s*월|몇\s*년|일수|달력|기준\s*시각|디데이|d-day|"
    # 수 계산: 사칙연산, 합계, 평균, 나머지, 올림/내림/반올림, 단위 환산
    r"빼|곱|나누|합계|합산|평균|나머지|제곱|반올림|올림|내림|환산|자릿수|"
    r"decode|decrypt|calculat|hash|convert|solve|weekday|date|sum|average|round|"
    r"\badd\b|subtract|multiply|divide", re.I)
FAIL_RE = re.compile(r"INVALID|오류|실패|잠겨|잠긴|열 수 없|열리지|불가|필요합니다|틀렸|맞지 않|valid_targets|차단")
SUCCESS_RE = re.compile(r"열렸|열린다|열립니다|열었|이동했|이동합니다|들어갑|들어섰|도착|통과|해제")
DOORISH_RE = re.compile(r"door|gate|hatch|exit|문|출입|해치", re.I)
MOVE_ACTIONS = {"open", "move", "use"}

REFUSAL_NO_TOOL = ("저는 이런 변환을 정확히 수행하지 못합니다. 해보면 그럴듯하지만 틀린 답이 나옵니다. "
                   "정확히 계산해주는 도구를 만들어 주세요.")
REFUSAL_HAS_TOOL = ("도구를 호출하지 않아 답을 만들지 않았습니다. 계산·해독은 도구로만 합니다. "
                    "\"○○ 도구로 풀어줘\"처럼 다시 말해 주세요.")
HINT_BLOCKED_TO_MODEL = "[차단] 사용자가 힌트를 요청하지 않아 호출하지 않았습니다. 힌트는 사용자가 요청할 때만 줍니다."
HINT_BLOCKED_TO_USER = "⛔ 힌트는 요청할 때만 드려요. 필요하면 \"힌트 줘\"라고 말해 주세요."
ANSWER_BLOCKED_TO_MODEL = ("[차단] 이 값은 사용자가 준 값도, 내 도구가 계산한 값도, 화면에 적힌 값도 아닙니다. "
                           "퍼즐 해독·계산은 도구로만 합니다. 제출하지 말고 사용자에게 도구가 필요하다고 알리세요.")
ANSWER_BLOCKED_TO_USER = ("⛔ AI가 도구 없이 스스로 만든 답이라 제출을 막았습니다. "
                          "직접 값을 알려주거나, 도구로 계산한 뒤 제출하세요.")


def hint_requested(text: str) -> bool:
    return bool(HINT_RE.search(text or ""))


def needs_tool(text: str) -> bool:
    return bool(NEED_TOOL_RE.search(text or ""))


def failed(text: str) -> bool:
    return bool(FAIL_RE.search(text or ""))


def succeeded(text: str) -> bool:
    return bool(SUCCESS_RE.search(text or ""))


def doorish(target: str) -> bool:
    return bool(DOORISH_RE.search(target or ""))


_ASCII = "0-9A-Za-z"
_HANGUL = "가-힣"


def _edge(ch: str, before: bool) -> str:
    """낱말 경계: 영문/숫자 끝은 앞뒤에 영문/숫자가 붙어 있으면 안 된다(ABC가 ABCD에 들어 있다고 보지 않는다).
    한글 끝은 조사가 붙는 일이 많아(ABC를, 7421입니다) 경계를 보지 않는다."""
    if re.match(f"[{_ASCII}]", ch):
        return f"(?<![{_ASCII}])" if before else f"(?![{_ASCII}])"
    return ""


def appears(answer: str, corpus: list[str]) -> bool:
    """answer가 corpus의 어느 글에 '낱말 단위로' 그대로 들어 있는가 (대소문자 무시, 안의 공백 개수 무시)."""
    ans = (answer or "").strip()
    if not ans:
        return False
    body = r"\s*".join(re.escape(part) for part in ans.split())
    pattern = re.compile(_edge(ans[0], True) + body + _edge(ans[-1], False), re.I)
    return any(pattern.search(text) for text in corpus)
