import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def roll_dice(n):
    import random
    rolls = []
    for _ in range(n):
        rolls.append(random.randint(1, 6))
    return rolls

def get_sum(rolls):
    return sum(rolls)

# 2. tool 목록 만들기 
tools = [
    {
        "type" : "function", 
        "name" : "roll_dice",
        "description" : "1부터 6까지의 정육면체 주사위를 n번 굴리고, 그 결과를 반환한다.",
        "parameters" : {
            "type" : "object", 
            "properties" : {
                "n" : {
                    "type" : "integer", 
                    "description" : "주사위를 굴릴 횟수"
                }
            },
            "required" : ["n"] 
        }   
    },
    {
        "type" : "function", 
        "name" : "get_sum",
        "description" : "주사위들의 합을 반환한다.",
        "parameters" : {
            "type" : "object", 
            "properties" : {
                "rolls" : {
                    "type" : "array", 
                    "items" : {
                        "type" : "integer"
                    },
                    "description" : "주사위들의 눈금이 담긴 container"
                }
            },
            "required" : ["rolls"] 
        }   
    }
]

# gpt한테 tool call을 시켜본다.
response = client.responses.create(
    model='gpt-4o-mini',
    input="주사위를 5번 굴리고, 나온 눈금들의 값을 순서대로 출력하고, 총 합을 구해줘.",
    tools=tools
)

print(response.output)

import json
while True: 
    messages = [] 
    for item in response.output:
        if item.type == "function_call":
            args = json.loads(item.arguments) 
            if item.name == "roll_dice":
                result = roll_dice(**args)
                print(result)
            elif item.name == "get_sum":
                result = get_sum(**args)
                print(result)
        
            #messages.append(item)
            messages.append({
                "type" : "function_call_output", # 필수 정의
                "call_id" : item.call_id, 
                "output" : str(result)
            })
    if not messages:
        break

    # 최종 프롬프트
    response = client.responses.create(
        model='gpt-4o-mini',
        input=messages,
        tools=tools,
        previous_response_id = response.id
    )

print(response.output_text)