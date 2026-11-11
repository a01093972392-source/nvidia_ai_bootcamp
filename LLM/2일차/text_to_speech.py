import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import base64


# 환경 변수 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Text to Speech 
result = client.audio.speech.create(
    model = 'gpt-4o-mini-tts',
    input = "기나긴 기다림 그 끝에 움켜쥔 한번의 반짝임 oh oh oh nah",
    voice= "shimmer"
)
# 추출
result.write_to_file("audio.mp3")

# STT (Speech to text)
# 1. transcription -> 단순하게 그냥 waveform을 역변환 -> text로 바꾼다.
# result = client.audio.transcriptions.create(
#     model= 'gpt-4o-mini-transcribe',
#     file = open("audio.mp3", 'rb') # 실제 mp3파일의 데이터를 binary로 넘겨준다.
# )
# print(result.text)

# 2. translation
# result = client.audio.translations.create(
#     model = "whisper-1", # 거의 죽은 모델 성능이 안좋음, 지원되지 않는 언어도 많음.
#     file = open("audio.mp3", 'rb')
# )
# print(result.text)

# 3. translation : transcription -> model에 번역을 맡긴다.
result = client.audio.transcriptions.create(
    model= 'gpt-4o-mini-transcribe',
    file = open("audio.mp3", 'rb') # 실제 mp3파일의 데이터를 binary로 넘겨준다.
)
response = client.responses.create(
    model = 'gpt-4o-mini',
    input = result.text,
    instructions = "너는 한영 번역가이다. 한글로 구성된 문장이 들어오면, 영어로 변환하라"
)
print(response.output_text)

