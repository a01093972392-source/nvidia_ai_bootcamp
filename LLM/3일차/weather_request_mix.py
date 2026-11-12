import os
from openai import OpenAI
from dotenv import load_dotenv
import requests # requst를 보내기 위한 라이브러리
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_location(city):
    # 경도 위도 찾아오기
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count" : 1,
        "language" : "en",
        "format" : "json" 
    }
    response = requests.get(
        url,
        params=params
    )
    print(response.status_code)
    latitude = response.json()['results'][0]['latitude']
    longitude = response.json()['results'][0]['longitude']
    return latitude, longitude

def get_temperature(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude" : longitude,
        "current": "temperature_2m", 
    }

    url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(
        url,
        params=params
    )
    print(response.status_code)
    return response.json()['current']['temperature_2m']

def get_weather(city):
    latitude, longitude = get_location(city)
    temperature = get_temperature(latitude, longitude)
    return {"city" : city, "temperature" : temperature}

tools = [
    {
        "type" : "function", 
        "name" : "get_weather",
        "description" : "특정 도시의 날씨를 알려준다.",
        "parameters" : {
            "type" : "object", 
            # tool call을 할때 전달해야 하는 파라미터들 정의
            "properties" : {
                # 하나의 파라미터 명
                "city" : {
                    "type" : "string", 
                    "description" : "도시의 이름. 사용자가 한글로 입력하면, 영어로 번역한다. 예) 서울-Seoul, 동경-Tokyo, 파리-Paris."
                }
            },
            "required" : ["city"] 
        }   
    }
]

import gradio as gr
import json
memory = [None]
def get_response(message):
    global memory
    # gpt한테 tool call을 시켜본다.
    response = client.responses.create(
        model='gpt-4o-mini',
        input=message,
        tools=tools,
        instructions="너는 토종 한국인이다. 모든 대답은 한국어로 한다.",
        previous_response_id = memory[-1]
    )

    if response.output_text:
        memory.append(response.id)
        return response.output_text

    try : 
        messages = []
        for item in response.output:
            if item.type == "function_call":
                args = json.loads(item.arguments)
                result = get_weather(**args)
                #print(result)
                messages.append(item)
                messages.append({
                    "type" : "function_call_output", # 필수 정의
                    "call_id" : item.call_id, 
                    "output" : str(result) 
                })

        response2 = client.responses.create(
            model='gpt-4o-mini',
            input=messages,
            tools=tools,
            instructions="너는 토종 한국인이다. 모든 대답은 한국어로 한다.",
            previous_response_id = memory[-1]
        )
        memory.append(response2.id)
        return response2.output_text
    except :
        return "죄송합니다. 요청을 처리하는 중 오류가 발생했습니다."

def reply(message, history):
    history = history + [{"role":"user", "content":message}]
    history = history + [{"role":"assistant", 'content':get_response(message)}]
    return "", history

with gr.Blocks() as app:
    chatbot = gr.Chatbot(height=600)
    message = gr.Textbox(label="message")

    message.submit(
        fn=reply,
        inputs=[message, chatbot],
        outputs=[message, chatbot]
    )

app.launch()