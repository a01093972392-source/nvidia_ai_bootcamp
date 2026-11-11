"""한국 속담 그림 퀴즈.

설치: python -m pip install -U gradio openai pillow
실행: python proverb_game.py
OPENAI_API_KEY 환경변수 또는 실행 시 비공개 입력 사용.
최초 실행에서 GPT가 속담 500개 후보를 생성합니다. 목록은 검증된 사전 데이터가
아니므로 proverbs_500.json에서 표현과 뜻을 검토/수정할 수 있습니다.
"""

import base64
import getpass
import hashlib
import io
import json
import math
import os
import random
import re
import time
import unicodedata
from pathlib import Path

import gradio as gr
from openai import OpenAI
from PIL import Image

IMAGE_MODEL = "gpt-image-1-mini"
TEXT_MODEL = "gpt-4o-mini"
TARGET_COUNT = 5
ROOT = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
BANK_FILE = ROOT / "proverbs_5.json"
CACHE_DIR = ROOT / "proverb_images"
client = None  # 기존 client가 있다면 이 줄을 client = 기존_client 로 변경 가능


def get_client():
    global client
    if client is None:
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY를 설정하거나 기존 client를 연결해주세요.")
        client = OpenAI(timeout=180.0, max_retries=1)
    return client


def normalize(text):
    text = unicodedata.normalize("NFC", text or "").lower()
    return re.sub(r"[^가-힣a-z0-9]", "", text)


def clean_bank(items):
    """형식과 정규화 중복 검사. 실제 속담 여부를 검증하는 함수는 아닙니다."""
    result, seen = [], set()
    for item in items:
        if not isinstance(item, dict):
            continue
        answer = item.get("answer")
        meaning = item.get("meaning")
        if not isinstance(answer, str) or not isinstance(meaning, str):
            continue
        key = normalize(answer)
        if not 4 <= len(key) <= 70 or not meaning.strip() or key in seen:
            continue
        seen.add(key)
        aliases = item.get("aliases", [])
        if not isinstance(aliases, list):
            aliases = []
        result.append({
            "answer": answer.strip(),
            "meaning": meaning.strip(),
            "aliases": [a.strip() for a in aliases if isinstance(a, str) and normalize(a)],
        })
    return result


def load_bank():
    if not BANK_FILE.exists():
        return []
    data = json.loads(BANK_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("proverbs_500.json의 최상위 값은 리스트여야 합니다.")
    return clean_bank(data)[:TARGET_COUNT]


def save_bank(bank):
    temporary = BANK_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(BANK_FILE)


def prepare_bank(progress):
    bank = load_bank()
    for _ in range(20):
        if len(bank) >= TARGET_COUNT:
            break
        progress(len(bank) / TARGET_COUNT, desc=f"속담 목록 준비 중: {len(bank)}/500")
        count = min(60, TARGET_COUNT - len(bank))
        excluded = [item["answer"] for item in bank]
        response = get_client().chat.completions.create(
            model=TEXT_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": (
                    "너는 한국 속담 퀴즈의 문제 편집자다. 한국에서 실제로 쓰이는 전통 속담만 "
                    "선정한다. 속담을 창작하지 않는다. 사자성어, 명언, 외국 격언, "
                    "표현만 다른 중복은 제외한다. 그림으로 표현할 수 있는 구체적인 소재를 "
                    "우선한다. aliases에는 같은 속담의 실제 통용 표현만 넣고 의미가 비슷한 "
                    "다른 속담은 넣지 않는다. 가족이 함께 풀 수 있는 표현을 선택한다. "
                    'JSON 형식: {"items":[{"answer":"속담", "meaning":"짧은 뜻", '
                    '"aliases":["동일 속담의 통용 표현"]}]}'
                )},
                {"role": "user", "content": (
                    f"중복되지 않는 한국 속담 {count}개를 JSON으로 반환해줘. "
                    "aliases가 없으면 빈 리스트로 해줘. 아래 목록 및 그 변형은 제외해줘:\n"
                    + json.dumps(excluded, ensure_ascii=False)
                )},
            ],
        )
        choice = response.choices[0]
        if choice.finish_reason != "stop":
            raise RuntimeError("속담 목록 응답이 중단됐습니다. 다시 시작하면 이어서 준비합니다.")
        data = json.loads(choice.message.content or "{}")
        if not isinstance(data.get("items"), list):
            raise ValueError("속담 응답 형식이 올바르지 않습니다. 다시 시작해주세요.")
        bank = clean_bank(bank + data["items"])[:TARGET_COUNT]
        save_bank(bank)  # 중간 실패 시에도 이어서 준비
    if len(bank) < TARGET_COUNT:
        raise RuntimeError(f"현재 {len(bank)}개 저장됨. 다시 시작하면 500개까지 이어서 준비합니다.")
    return bank


def create_picture(item):
    CACHE_DIR.mkdir(exist_ok=True)
    key = hashlib.sha256((IMAGE_MODEL + "|v1|" + item["answer"]).encode()).hexdigest()
    path = CACHE_DIR / f"{key}.png"
    if path.exists():
        try:
            with Image.open(path) as image:
                return image.convert("RGB").copy()
        except OSError:
            path.unlink(missing_ok=True)
    response = get_client().images.generate(
        model=IMAGE_MODEL,
        prompt=(
            "한국 속담을 맞히는 그림 퀴즈용 이미지 한 장을 그려줘. "
            "흰색 그림판에 사람이 색연필과 굵은 펜으로 그린 듯한 간단하고 귀여운 그림. "
            "속담의 핵심 사물과 행동, 관계를 한 장면 또는 2~3개의 장면으로 표현해줘. "
            "그림만 보고 추측할 수 있게 해줘. "
            "글자, 한글, 영어, 숫자, 자막, 말풍선, 제목, 정답은 절대로 그리지 마. "
            f"표현할 속담: {item['answer']}\n의미: {item['meaning']}"
        ),
        size="1024x1024",
        quality="low",
        n=1,
    )
    if not response.data or not response.data[0].b64_json:
        raise RuntimeError("그림이 반환되지 않았습니다. 다음 문제를 눌러 다시 시도해주세요.")
    with Image.open(io.BytesIO(base64.b64decode(response.data[0].b64_json))) as image:
        picture = image.convert("RGB").copy()
    picture.save(path, format="PNG")
    return picture


def new_state(seconds=60):
    return dict(bank=[], order=[], cursor=0, current=None, phase="idle",
                deadline=0.0, seconds=int(seconds), score=0, total=0, message="")


def reveal_answer(state, reason):
    if state["phase"] != "playing":
        return
    item = state["current"]
    state["phase"] = "revealed"
    state["message"] = f"{reason}\n\n**정답: {item['answer']}**\n\n뜻: {item['meaning']}"


def render(state, picture=None, change_picture=False, answer_value=None):
    playing = state["phase"] == "playing"
    busy = state["phase"] == "loading"
    left = max(0, math.ceil(state["deadline"] - time.monotonic())) if playing else 0
    info = (f"### ⏱️ 남은 시간: {left}초\n"
            f"문제 {state['total']} · 정답 {state['score']}개 · 목록 {len(state['bank'])}개")
    # 타이머 업데이트에서 입력 중인 답과 이미지를 덮어쓰지 않는다.
    answer_update = {"interactive": playing}
    if answer_value is not None:
        answer_update["value"] = answer_value
    return (
        state,
        picture if change_picture else gr.skip(),
        info,
        state["message"],
        gr.update(**answer_update),
        gr.update(interactive=playing),
        gr.update(interactive=playing),
        gr.update(interactive=state["phase"] in {"revealed", "error"} and bool(state["bank"])),
        gr.update(interactive=not busy),
        gr.update(active=playing),
    )


def advance(state):
    """이미지가 준비된 뒤에만 문제 수와 타이머를 갱신한다."""
    if not state["bank"]:
        raise RuntimeError("먼저 게임 시작을 눌러주세요.")
    if state["cursor"] >= len(state["order"]):
        state["phase"] = "complete"
        state["message"] = f"🎉 모든 문제 완료! {state['total']}문제 중 {state['score']}개 정답입니다."
        return render(state, answer_value="")
    index = state["order"][state["cursor"]]
    picture = create_picture(state["bank"][index])
    state["cursor"] += 1
    state["current"] = state["bank"][index]
    state["total"] += 1
    state["phase"] = "playing"
    state["deadline"] = time.monotonic() + state["seconds"]
    state["message"] += "\n\n그림이 나타났습니다. 속담을 입력해주세요!"
    return render(state, picture, True, answer_value="")


def fail(state, error):
    state["phase"] = "error"
    state["message"] += f"\n\n⚠️ {type(error).__name__}: {error}"
    return render(state)


def start(seconds, old_state, progress=gr.Progress()):
    state = new_state(seconds)
    state["phase"] = "loading"
    state["message"] = "속담 목록과 첫 번째 그림을 준비합니다. 처음에는 시간이 걸립니다."
    yield render(state, None, True, answer_value="")
    try:
        state["bank"] = prepare_bank(progress)
        state["order"] = random.sample(range(len(state["bank"])), len(state["bank"]))
        state["message"] = "새 게임을 시작했습니다."
        progress(0.98, desc="첫 번째 그림 생성 중")
        yield advance(state)
    except Exception as error:
        yield fail(state, error)


def next_question(state):
    if state["phase"] not in {"revealed", "error"} or not state["bank"]:
        yield render(state)
        return
    state["phase"] = "loading"
    state["message"] = "다음 그림을 준비합니다…"
    yield render(state)
    try:
        state["message"] = ""
        yield advance(state)
    except Exception as error:
        yield fail(state, error)


def submit_answer(text, state):
    if state["phase"] != "playing":
        yield render(state)
        return
    if time.monotonic() >= state["deadline"]:
        reveal_answer(state, "⌛ 시간이 끝났습니다!")
        yield render(state)
        return
    item = state["current"]
    accepted = {normalize(a) for a in [item["answer"], *item["aliases"]]}
    if not normalize(text):
        state["message"] = "속담을 입력해주세요."
        yield render(state)
        return
    if normalize(text) not in accepted:
        state["message"] = "아직 정답이 아니에요. 다시 입력하거나 ‘정답 보기’를 눌러주세요."
        yield render(state)
        return
    state["score"] += 1
    state["phase"] = "loading"
    state["message"] = f"✅ 정답! **{item['answer']}**\n\n뜻: {item['meaning']}\n\n다음 그림 준비 중…"
    yield render(state, answer_value="")
    try:
        # 정답 피드백은 다음 그림이 준비된 뒤에도 남겨둔다.
        yield advance(state)
    except Exception as error:
        yield fail(state, error)


def give_up(state):
    reason = "⌛ 시간이 끝났습니다!" if time.monotonic() >= state["deadline"] else "🔎 정답 공개"
    reveal_answer(state, reason)
    return render(state)


def tick(state):
    if state["phase"] == "playing" and time.monotonic() >= state["deadline"]:
        reveal_answer(state, "⌛ 시간이 끝났습니다!")
    return render(state)


def build_demo():
    with gr.Blocks(title="속담 그림 퀴즈") as demo:
        state = gr.State(new_state())
        timer = gr.Timer(1, active=False)
        gr.Markdown("# 🎨 속담 그림 퀴즈\nGPT가 그린 그림을 보고 속담을 맞혀보세요.")
        with gr.Row():
            seconds = gr.Slider(15, 180, value=60, step=5, label="문제당 제한 시간 (새 게임에 적용)")
            start_btn = gr.Button("게임 시작 / 처음부터", variant="primary")
        with gr.Row():
            with gr.Column(scale=3):
                picture = gr.Image(label="이 그림은 어떤 속담일까요?", type="pil", format="png",
                                   height=520, interactive=False)
            with gr.Column(scale=2):
                info = gr.Markdown("### 게임 시작을 눌러주세요")
                message = gr.Markdown("처음에는 속담 500개 후보를 준비합니다. 그림 생성 시간은 제한 시간에 포함되지 않습니다.")
                answer = gr.Textbox(label="정답 입력", placeholder="속담을 입력하고 Enter", interactive=False)
                submit_btn = gr.Button("정답 제출", variant="primary", interactive=False)
                reveal_btn = gr.Button("모르겠어요 · 정답 보기", interactive=False)
                next_btn = gr.Button("다음 문제", interactive=False)
        gr.Markdown("띄어쓰기·문장부호는 무시합니다. 정답이면 자동으로 다음 문제로 넘어갑니다. "
                    "시간 초과 또는 정답 공개 후에는 ‘다음 문제’를 누르세요. "
                    "속담 목록은 GPT가 만든 후보이므로 검토가 필요합니다.")
        outputs = [state, picture, info, message, answer, submit_btn, reveal_btn, next_btn, start_btn, timer]
        shared = dict(outputs=outputs, concurrency_id="game", concurrency_limit=1)
        start_btn.click(start, inputs=[seconds, state], **shared)
        next_btn.click(next_question, inputs=[state], **shared)
        submit_btn.click(submit_answer, inputs=[answer, state], **shared)
        answer.submit(submit_answer, inputs=[answer, state], **shared)
        reveal_btn.click(give_up, inputs=[state], **shared)
        timer.tick(tick, inputs=[state], show_progress="hidden", trigger_mode="once", **shared)
    return demo


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API 키 (화면에 표시되지 않음): ").strip()
    demo = build_demo()
    demo.queue().launch(inbrowser=True)
