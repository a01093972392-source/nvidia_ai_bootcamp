from fastmcp import Client
import asyncio   # 동기 / 비동기화
from openai import OpenAI
from dotenv import load_dotenv
import os

client = Client("server.py")

# async def main() :
#     async with client :
#         # 날씨를 물어보기
#         weather_result = await client.call_tool("get_weather")
#     weather = weather_result.content[0].text
#     print(weather)

#     async with client :
#         # 활동 추천
#         activity_result = await client.call_tool(
#             "recommend_activiy",
#             {"weather" : weather}
#         )
#     activity = activity_result.content[0].text
#     print(activity)
#     async with client :
#             # 점심 추천
#             lunch_result = await client.call_tool(
#                 "recommend_lunch",
#                 {"activity" : activity}
#             )
#     lunch = lunch_result.content[0].text
#     print(lunch)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)


async def main():
    async with client:
        tool_list = await client.list_tools()
        # print(tool_list)

    tools = []
    for tool in tools:
        # openai responses api ... {tools = tools}
        tools.append({
            "type" : "function",
            "name" : tool.name,
            "description" : tool.description,
            "parameters" : tool.input_schema
        })
        response = openai_client.responses.create(
            model = 'gpt-4o-mini',
            input = "오늘 비가 오는데, 뭘 하면 좋을까?",
            tools = tools
        )
        # tool 호출에 대한 제안서가 나올것
        tool_results = []
        for item in response.output:
            if item.type == "function_call":
                result = await client.call_tool(item.name)
                tool_results.append({
                    "type" : "function_call_output",
                    "call_id" : item.call_id,''
                    "output" : str(result.data)
                })

        if len(tool_results) > 0:
            response = openai_client.responses.create(
                model = 'gpt-4o-mini',
                input = tool_results,
                previous_response_id= response.id
            )

        print(response.output_text)

asyncio.run(main())
