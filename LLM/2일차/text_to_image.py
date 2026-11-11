import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import base64


# 환경 변수 불러오기
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# text to image
# 이미지 생성
result = client.images.generate(
    model = "gpt-image-1-mini",                              # 이미지 생성은 gpt-4ㅐ-mini가 해결할 수 없음.
    prompt = "홍콩 야시장 풍경에서 푸드트럭 안에서 열심히 한국의 불닭볶음면계란말이를 팔고 있는 잘생긴 한국남자를 그려주고 푸드트럭 주변에 인기를 실감할 수 있는 풍경을 그려줘",
    size = "1024x1024"
)
# result -> 이미지를 만들기는 하는데 -> img 파일처럼 나오는게 아님
# 64bit의 형태의 데이터 뭉텅이가 나옴
image_base64 = result.data[0].b64_json

with open("Buldak.png", 'wb') as f:
    f.write(base64.b64decode(image_base64))