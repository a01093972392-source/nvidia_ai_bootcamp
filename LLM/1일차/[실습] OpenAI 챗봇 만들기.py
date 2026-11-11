
import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

# 1. .env에서 환경 변수 불러오기
# .env에 OPENAI_API_KEY=본인의_API_키 를 작성한 뒤 실행하세요.
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# temperature 설정을 사용할 수 있는 GPT 모델입니다.
MODEL = "gpt-4o-mini"
DEFAULT_INSTRUCTION = "당신은 친절한 AI 도우미입니다. 사용자의 질문에 한국어로 답하세요."
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500

TOKEN_CHOICES = [50, 100, 200, 500, 1000]


# 2. 설정완료 버튼: 세 UI 값을 받아 실제 대화에 적용할 설정을 저장합니다.
def setting_sync(instruction, temperature, max_output_tokens):
    settings = {
        "instruction": instruction.strip(),
        "temperature": float(temperature),
        "max_output_tokens": int(max_output_tokens),
    }
    # 이 반환값은 아래 control_outputs의 순서와 일치합니다.
    return (
        settings, [], [],
        gr.update(value=settings["instruction"], interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=True),
        gr.update(value="", interactive=True),
        gr.update(interactive=True),
        f"설정 완료 | {MODEL} | temperature={settings['temperature']} | "
        f"max_output_tokens={settings['max_output_tokens']}",
    )


# 3. 대화: 저장된 설정과 지금까지의 대화 내용을 함께 API에 전달합니다.
def chat(message, history, settings):
    messages = [dict(item) for item in history]
    messages.append({"role": "user", "content": message})

    response = client.responses.create(
        model=MODEL,
        instructions=settings["instruction"],
        temperature=settings["temperature"],
        max_output_tokens=settings["max_output_tokens"],
        input=messages,
        store=False,
    )

    messages = messages + [{"role": "assistant", "content": response.output_text}]
    return messages, messages, "", "답변 완료"


# 4. 화면과 API에 전달하는 대화기록을 모두 삭제합니다. 설정은 유지합니다.
def clear_history():
    return [], [], "", "대화기록을 삭제했습니다. 현재 모델 설정은 유지됩니다."


# 5. 설정과 대화를 초기화하고, 설정 UI를 다시 활성화합니다.
def reset_settings():
    return (
        None, [], [],
        gr.update(value=DEFAULT_INSTRUCTION, interactive=True),
        gr.update(value=DEFAULT_TEMPERATURE, interactive=True),
        gr.update(value=DEFAULT_MAX_TOKENS, interactive=True),
        gr.update(interactive=True),
        gr.update(interactive=False),
        gr.update(value="", interactive=False),
        gr.update(interactive=False),
        "초기화했습니다. 설정을 입력하고 설정완료 버튼을 눌러주세요.",
    )


# 6. Gradio UI 구성
with gr.Blocks(title="나만의 GPT 챗봇") as demo:
    # 사용자별로 설정과 대화를 분리합니다. 전역 변수에 대화를 저장하지 않습니다.
    settings_state = gr.State(value=None)
    history_state = gr.State(value=[])

    gr.Markdown("# 나만의 GPT 챗봇\n설정완료 버튼을 누른 뒤 대화를 시작하세요.")
    with gr.Row():
        with gr.Column(scale=1):
            instruction = gr.Textbox(
                label="instruction", value=DEFAULT_INSTRUCTION, lines=5,
                placeholder="챗봇의 역할과 답변 방식을 입력하세요.",
            )
            temperature = gr.Slider(
                label="temperature", minimum=0, maximum=2, step=0.1,
                value=DEFAULT_TEMPERATURE,
            )
            max_output_tokens = gr.Radio(
                label="max_output_tokens", choices=TOKEN_CHOICES,
                value=DEFAULT_MAX_TOKENS,
            )
            setting_button = gr.Button(value="설정완료", variant="primary")
            reset_button = gr.Button(value="재설정", interactive=False)

        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="GPT와 대화", height=450)
            message = gr.Textbox(
                label="메시지", placeholder="설정을 완료한 뒤 입력하세요.",
                interactive=False,
            )
            with gr.Row():
                send_button = gr.Button(value="전송", interactive=False, variant="primary")
                clear_button = gr.Button(value="대화기록 삭제")

    status = gr.Textbox(
        label="상태", value="설정을 입력하고 설정완료 버튼을 눌러주세요.",
        interactive=False,
    )

    control_outputs = [
        settings_state, history_state, chatbot, instruction, temperature,
        max_output_tokens, setting_button, reset_button, message, send_button, status,
    ]

    # 모든 이벤트가 같은 대기열을 사용하므로 답변 도중 초기화하더라도
    # 초기화 뒤에 오래된 답변이 다시 표시되는 일을 방지합니다.
    event_options = {"concurrency_id": "chatbot_events", "concurrency_limit": 1}
    setting_button.click(
        fn=setting_sync,
        inputs=[instruction, temperature, max_output_tokens],
        outputs=control_outputs,
        **event_options,
    )
    send_button.click(
        fn=chat, inputs=[message, history_state, settings_state],
        outputs=[history_state, chatbot, message, status],
        **event_options,
    )
    message.submit(
        fn=chat, inputs=[message, history_state, settings_state],
        outputs=[history_state, chatbot, message, status],
        **event_options,
    )
    clear_button.click(
        fn=clear_history, inputs=None,
        outputs=[history_state, chatbot, message, status],
        **event_options,
    )
    reset_button.click(
        fn=reset_settings, inputs=None, outputs=control_outputs,
        **event_options,
    )


if __name__ == "__main__":
    demo.queue().launch()
