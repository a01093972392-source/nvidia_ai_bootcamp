import os
from openai import OpenAI
from dotenv import load_dotenv
import requests # requst를 보내기 위한 라이브러리
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 경도 위도 찾아오기
url = "https://geocoding-api.open-meteo.com/v1/search"
city = input()
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

latitude = response.json()['results'][0]['latitude']
longitude = response.json()['results'][0]['longitude']

# 이 웹사이트에 우리는 요청을 보내볼것이다.
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
#print(response.json())
print(response.json()['current']['temperature_2m'])