import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import base64


# 환경 변수 불러오기
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# image edit
# image -> image
result = client.images.edit(
    model = 'gpt-image-1-mini',
    image=open("Buldak.png", 'rb'),     # 'rb' = read binary -> 이미지를 
    prompt = "남자를 여자로 바꿔줘, 그리고 푸드트럭 앞에 사람이 많은걸로 바꿔줘"
)

image_base64 = result.data[0].b64_json

with open("Buldak_revise.png", 'wb') as f:
    f.write(base64.b64decode(image_base64))
