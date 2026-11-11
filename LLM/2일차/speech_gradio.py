import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import base64


# 환경 변수 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def transcribe(audio):
    with open(audio, 'rb') as f:
        result = client.audio.transcriptions.create(
            model = 'gpt-4o-mini-transcribe',
            file = f
        )
    return result.text

# gradio speech component
with gr.Blocks() as demo:
    audio = gr.Audio(
        # 1. 어디에서 내 음성 소스를 집어넣을거냐
        sources = ['microphone', 'upload'],
        type = "filepath",
        label = "마이크 입력"
    )
    btn = gr.Button(
        "transcribe"
    )
    text = gr.Textbox(
        label = "출력"
    )
    btn.click(
        fn = transcribe,
        inputs= [audio],
        outputs= text
    )

demo.launch()