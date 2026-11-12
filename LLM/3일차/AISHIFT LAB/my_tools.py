"""여기가 여러분이 작업할 파일입니다.

게임을 하다 막히면 **필요한 기능을 이 파일에 직접 만드세요.**
`@mcp.tool`을 붙인 함수는 자동으로 AI가 쓸 수 있는 도구가 됩니다.

규칙은 두 가지뿐입니다.
  1. 함수에 타입을 적는다      (text: str, rotate: int -> str)
  2. 함수에 설명을 적는다      (docstring)

AI는 이 설명을 읽고 언제 이 도구를 쓸지 판단합니다.
설명이 부실하면 도구를 만들어도 AI가 쓰지 않거나, 엉뚱하게 씁니다.
"""

import datetime
import hashlib

import requests
from fastmcp import FastMCP

mcp = FastMCP("my-tools")



# ─────────────────────────────────────────────────────────────
# 여기부터 여러분의 도구를 만드세요.
#
# @mcp.tool
# def 함수이름(인자: 타입) -> 반환타입:
#     """이 도구가 무엇을 하는지 한 줄로 설명합니다."""
#     ...
# ─────────────────────────────────────────────────────────────@mcp.tool
@mcp.tool
def decoded_code(code: str) -> str:
  result = ""

  for char in code.upper():
    if "A" <= char <= "Z":
      result += chr((ord(char) - ord("A") - 4) % 26 + ord("A"))
    else:
      result += char  # 띄어쓰기 등은 그대로 유지
  
  return result  

# WEATHER_CODE = (floor(TEMP_C) + 50) * 10 + floor(HUMIDITY / 10) 

import math
import requests

import math
import requests
from datetime import datetime


@mcp.tool
def get_weather_code(city: str, reference_time: str) -> dict:
    """서울의 지정 시각 기온, 습도, 계산한 날씨 코드를 반환합니다."""
    if city.strip().lower() not in ("seoul", "서울"):
        raise ValueError("현재 지원하는 도시는 seoul(서울)입니다.")

    normalized_time = reference_time.strip().replace(" ", "T")
    if len(normalized_time) > 10 and normalized_time[10] == "-":
       normalized_time = normalized_time[:10] + "T" + normalized_time[11:]

    dt = datetime.strptime(normalized_time, "%Y-%m-%dT%H:%M")

    if dt.minute != 0:
        raise ValueError("시간은 16:00처럼 정시로 입력해주세요.")

    date = dt.strftime("%Y-%m-%d")

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 37.5665,
            "longitude": 126.9780,
            "hourly": "temperature_2m,relative_humidity_2m",
            "timezone": "Asia/Seoul",
            "start_date": date,
            "end_date": date,
        },
        timeout=15,
    )
    response.raise_for_status()
    hourly = response.json()["hourly"]

    index = hourly["time"].index(dt.strftime("%Y-%m-%dT%H:%M"))
    temp_c = hourly["temperature_2m"][index]
    humidity = hourly["relative_humidity_2m"][index]

    if temp_c is None or humidity is None:
        raise ValueError("해당 시각의 기온 또는 습도 데이터가 없습니다.")

    return {
        "TEMP_C": temp_c,
        "HUMIDITY": humidity,
        "WEATHER_CODE": (
            (math.floor(temp_c) + 50) * 10
            + math.floor(humidity / 10)
        ),
    }

import hashlib


@mcp.tool
def get_safe_code(beta: str) -> str:
    """BETA를 입력받아 금고 복구 코드 6자리를 반환합니다."""
    source = f"XXAU:{beta}"
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()

    return digest[:6]


from datetime import datetime, timedelta, timezone


@mcp.tool
def get_exit_code(exit_nonce: int) -> str:
    """EXIT_NONCE와 한국 기준 오늘 날짜로 비상 해제 코드를 계산합니다."""
    kst = timezone(timedelta(hours=9))
    day_of_year = datetime.now(kst).timetuple().tm_yday

    exit_code = (exit_nonce + day_of_year) % 10000

    return f"{exit_code:04d}"