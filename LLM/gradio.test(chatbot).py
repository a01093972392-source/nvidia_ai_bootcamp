# ML / LLM 서비스를 위한 가볍게 UI를 만들수 있는 툴

import gradio as gr

# Chatbot interface는 대화의 내용을 'messages'라는 리스트로 반환
# messages내 각 message는 "누가 말했는지"와 어떤 말(content)을 했는지를 딕셔너리의 형태로 저장한다.
def reply(message, history):
    # 메뉴얼로 일단 내가 지금 입력한 값을 -> history에 누적을 시켜야함
    history = history + [
        {"role" : "user", "content": message}
    ]
    # 당연히 원래는 -> gpt가 주는 respoonse
    response = message + "에 대한 답변입니다."

    # assistant에 답변도 history에 저장을 해줘야함
    history = history + [
        {"role" : "assistant", "content" : response}
    ]
    return "", history



with gr.Blocks() as demo:
    chatbot = gr.Chatbot() # chatbot interface
    msg = gr.Textbox(label="message")

    msg.submit(
        fn = reply,
        inputs = [msg, chatbot],
        outputs=[msg, chatbot]
    )

demo.launch()