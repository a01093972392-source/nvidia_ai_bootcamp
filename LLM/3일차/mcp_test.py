import os
from openai import OpenAI
from dotenv import load_dotenv
import requests # requst를 보내기 위한 라이브러리
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

