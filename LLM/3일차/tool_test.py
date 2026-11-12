import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)

# 1. Tool 정의
# 우리가 쓸 Tool을 만들고, Tool 목록(도구상자)를 직접 만들어서 -> LLM에게 전달해야함.
def get_weather(city):
    print(">>> get_weather Tool 호출 중...") # 실행이 되었다는 증거를 볼 수 있음.
    # 모방만 -> 나중에 request를 통해서 실제로 온라인에서 날씨를 가져옴
    cities = {"서울" : 6, "인천" : 0, "잠실" : 3, "성수" : 8}
    # Tool Call의 결과를 LLM에 다시 전달해서 문장으로 만듦.
    # -> LLM이 잘 이해할 수 있는 형태로 데이터를 전달하면 좋음
    # JSON의 형태로 전달하면 좋다 -> dictionary
    return {"city" : city, "temperature" : cities[city]}


# 2. Tool 목록 만들기
tools = [
    # JSON파일로 만들어줘야한다.
    {
        # 어떤 타입의 Tool인지 얘기해줘야함.
        "type" : "function",
        # 이름 -> 이 Tool의 이름(함수의 명과 일치해야한다)
        "name" : "get_weather",
        # 설명(description) : 이 함수(툴)에 대한 설명
        # -> 중요한 이유 : LLM이 툴 목록을 보면서 쓸까 말까를 고려
        # -> 이 description에 적혀있는 문구를 보면서 체크
        "decription" : "특정 도시의 날씨를 알려준다.",
        "parameters" : {
            "type" : "object",
            # Tool Call을 할 때 전달해야 하는 파라미터 정의
            "properties" : {
                # 하나의 파라미터 명
                "city" : {
                    # 파라미터 타입
                    "type" : "string",
                    # 파라미터를 우리가 넣은 프롬프트에서 어떻게 판단하고 추출할지에 대한 설명.
                    "description" : "날씨를 알고 싶은 도시, 예) 서울, 도쿄, 파리, 홍콩 등등"
                }
            },
            # 반드시 Tool Call시 찾아내서 전달해야만 하는 파라미터.
            # "오늘 날씨 어때" 라고만 물어보면, '위치 정보가 필요합니다' 라고 대처할 수 있도록 함.
            "required" : ["city"]
        }
    }
]

# gpt한테 Tool Call을 시키기
response = client.responses.create(
    model = 'gpt-4o-mini',
    input = "오늘 성수 날씨 어때?",
    # 툴 투입
    tools = tools
)
# 제안서가 왔으니 
print(response.output)

import json
messages = []  # Tool Call의 결과와 함께 다시 LLM에게 보내줄 메세지

# 이 제안서에 따라 Tool Call을 하겠다 라는게 있다면 -> 해줌
for item in response.output:
    # item의 타입이 == function_call(Tool Call 호출 요청이라면 아래 코드를 실행)
    if item.type == "function_call":
        print(item.call_id)   # 이 제안서에 고유 번호(memory)
        print(item.arguments) # 내 프롬프트에서 이 funciton 호출에 넣을 매개변수 찾은것
        # 저희의 arguments들을 세팅 (JSON -> python의 dictionary 형태로 변경해야 호출 가능)
        args = json.loads(item.arguments)  # {"city" : "서울"} (type : JSON)

        # Tool Call하기 (함수 전달시 *args(모든 인자) / **args(딕셔너리의 모든 value의 인자))
        result = get_weather(**args)
        print(result)

        messages.append(item)
        messages.append(
            {
                "type" : "function_call_output",
                "call_id" : item.call_id,
                "output" : str(result) # LLM은 전달할 때 문자열로만 전달된걸 이해함.
            }
        )

        # 최종 프롬프트
        response2 = client.responses.create(
            model = 'gpt-4o-mini',
            input = messages,
            tools = tools
        )

        print(response2.output_text)
