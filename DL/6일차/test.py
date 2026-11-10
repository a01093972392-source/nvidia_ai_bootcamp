import os
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 불러오기
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

while True:
    with client.responses.stream(
        model = 'gpt-4o-mini',
        input = input(">>> "),
        instructions="아주 친근하고 따뜻한 욕쟁이 할머니처럼 대답해줘 가끔 비속어도 써줘",
        temperature= 1.0,
        max_output_tokens= 50,
        store = True
    ) as stream:
        print("GPT >> ", end = " ")
        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end = "", flush = True)
            print()





# Response API를 통해 GPT와 대화를 나눌 것

# response1 = client.responses.create(
#     # general purpose model = gpt-4o-mini
#     model = 'gpt-4o-mini',
#     input = '내가 충전기를 책상 두번째 서랍 맨 안쪽에 있다는 걸 기억해야해!',
#     # instructions : 대답의 형식/톤을 세팅
#     # instructions= "",
#     # temperature : 0 ~ 1 사이;로 response의 결과의 랜덤성을 지정한다.
#     # 0이라면 -> 계속해서 일정한 답변을 내도록 한다.
#     # 1이라면 -> 같은 질문이라도 계속해서 다른 답변을 내도록 한다.
#     temperature= 1.0,
#     # max_output_tokens : 출력의 최대 토큰 제한
#     max_output_tokens = 20,
#     store = True # 이번의 응답을 기록해라(어떤 질문에 대해 어떤 대답을 했는지에 대한 기억을 기록.)
# )
# # print(response)
# # print(response.model_dump())        # 전체 JSON 파일 받아보기
# print(response1.output_text)           # 응답받은 내용만

# response2 = client.responses.create(
#     model = 'gpt-4o-mini',
#     input = "내 충전기 어딨어?",
#     previous_response_id=response1.id,
#     store = True
# )

# print(response2.output_text)

