# code here
import os
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 불러오기
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

