import os

import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 불러오기
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


# image to text
# image를 넣으면 text가 나오도록하는 multimodal의 형태를 써본다.

response = client.responses.create(
    model = 'gpt-4o-mini',
    # JSON의 형태로 보낸다.
    # -> 이미지와 이미지로 무엇을 할꺼냐에 대한 프롬프트르 보내야한다.
    input = [
        {
            "role" : "developer",
            "content" : """
            너는 이미지 분석 전문가야. 지금 보여지는 이미지를 다음과 같이 출력해줘
            [예시] 
            이미지 요약 : 3줄내로
            """
        },
        {
            "role":"user", # user가 보내는 것이다
            "content" : [
                # 우리가 이미지를 기반으로 뭔가를 하고싶은 컨텐츠
                {
                    "type" : "input_text", 
                    "text" : "지금 내가 준 그림을 3줄 내로 설명해줘."
                },
                # 실제 첨부할 이미지 또는 파일
                {
                    "type" : "input_image", 
                    "image_url" : "https://i.namu.wiki/i/B0fGYqdFyqRYZtdjyIrRMqEEYJqGS-z5tyHbQ0_d8hvu4X5mNB7oG1Dxyl12kk0Ldh5Qis1OZwdh3SNiEHFJAFDW38uYKP0k_r-1spDFqvOs2ve0I5g2n4QEZ82VHkYYBCkja5TPDMFkF8Becd-tNQ.webp"
                }
            ]
        }
    ]
)

print(response.output_text)