from fastmcp import FastMCP
import random

mcp = FastMCP("my server")

# 이 서버에서 쓸 수 있는 툴

@mcp.tool
def greeting(name):
    """이것은 이름이 주어지면, 그냥 인사를 할 때 사용됩니다."""
    return "Hello" + name


# 3개의 Tool
@mcp.tool
# 1. 날씨 가져오기
def get_weather():
    "오늘의 날씨를 알려줄 때 사용합니다."
    choices = ["비", "눈", "태풍", "바람", "흐림", "화창", "습함"]
    return random.choice(choices)
# 2. 이 날씨를 기반으로 오늘의 활동 추천하기
@mcp.tool
def recommend_activiy(weather):
    "주어진 날씨에 추천할만한 활동을 추천합니다."
    if weather == "비":
        return "비 맞기"
    elif weather == "눈":
        return "눈사람"
    elif weather == "태풍":
        return "집"
    elif weather =="바람":
        return "연날리기"
    elif weather == "흐림":
        return "영화관람"
    elif weather == "화창":
        return "한강가기"
    elif weather =="습함":
        return "땀내기"
# 3. 추천한 활동을 기반으로 점심 추천하기
@mcp.tool
def recommend_lunch(activity):
    "이 활동에서 어울리는 식사/간식을 추천합니다."
    if activity == "집":
        return "비 맞기"
    elif activity == "눈사람":
        return "호떡"
    elif activity == "집":
        return "해물파전"
    elif activity == "연날리기":
        return "엽떡"
    elif activity == "영화관람":
        return "팝콘"
    elif activity == "한강가기":
        return "한강라면"
    elif activity == "땀내기":
        return "냉면"


if __name__ == "__main__":
    mcp.run()