import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from openai import OpenAI, OpenAIError
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
KST = timezone(timedelta(hours=9))


def read_birthdate():
    while True:
        year = input("태어난 연도 (예: 1998): ").strip()
        month_day = input("태어난 월일 (양력, 예: 03-21): ").strip()
        try:
            if len(year) != 4 or not year.isdecimal():
                raise ValueError
            birthdate = date.fromisoformat(f"{year}-{month_day}")
            if birthdate > datetime.now(KST).date():
                raise ValueError
            return birthdate
        except ValueError:
            print("미래가 아닌 실제 생년월일을 입력해주세요. 월일은 MM-DD 형식입니다.\n")


def read_gender():
    choices = {"남": "남성", "남성": "남성", "여": "여성", "여성": "여성",
               "기타": "기타", "미입력": "미입력"}
    while True:
        gender = input("성별 (남성/여성/기타/미입력): ").strip()
        if gender in choices:
            return choices[gender]
        print("남성, 여성, 기타, 미입력 중 하나를 입력해주세요.")


def main():
    if not api_key or not api_key.strip():
        print("fortune_bot.py와 같은 폴더의 .env에 OPENAI_API_KEY를 설정해주세요.")
        return

    client = OpenAI(api_key = api_key)
    print("오늘의 운세봇입니다. '오늘의 운세를 알려줘'를 입력하세요. (종료: 종료)")

    while True:
        command = input("\n나: ").strip()
        if command.lower() in {"종료", "exit", "quit"}:
            print("다음에 또 만나요!")
            return
        if "오늘의운세" not in "".join(command.split()):
            print("'오늘의 운세를 알려줘'를 입력해주세요.")
            continue

        birthdate = read_birthdate()
        gender = read_gender()
        today = datetime.now(KST).date().isoformat()
        print("\n자료를 검색하고 운세를 작성하고 있습니다...\n")

        try:
            response = client.responses.create(
                model = 'gpt-4o-mini',
                input = f"""
                오늘의 운세를 알려줘.
                기준 날짜: {today} (한국 시간)
                생년월일: {birthdate.isoformat()} (양력)
                성별: {gender}
                출생 시간과 출생 장소는 제공되지 않았어.

                다음 순서로 한국어로 알기 쉽게 작성해줘.
                1. 전체적인 운세: 전반적인 성향, 강점, 주의할 점
                2. 오늘의 운세: 총운, 금전운, 연애·대인관계운, 일·학업운
                3. 오늘 실천하면 좋은 행동과 한 줄 조언
                4. 참고 자료: 실제 검색해서 확인한 자료의 제목과 URL
                """,
                instructions = """
                너는 세계적으로 유명한 사주와 타로를 봐주는 사람처럼
                친절하게 전통 운세를 해석해주는 상담가야.
                신뢰할 수 있는 웹페이지와 고서의 공개 원문·해설을 웹 검색으로
                확인해 전통적 해석의 배경을 참고해줘. 기관·도서관·박물관 자료를 우선해.
                생년월일이나 성별 같은 개인 정보는 검색어에 포함하지 말고,
                전통 운세의 일반적인 개념을 검색해줘.
                검색에서 확인하지 않은 출처나 고서의 문구를 지어내지 마.
                자료가 부족하면 그 한계를 밝혀줘.
                출생 시간이 없고 만세력을 계산하지 않았으므로 정확한 사주팔자나
                대운을 산출했다고 주장하지 마. 실제 타로 카드를 뽑았다고 하지 마.
                전통 자료의 설명과 사용자를 위한 창작 해석을 구분해줘.
                운세는 재미와 자기 성찰을 위한 참고용이며 미래를 확정하는
                과학적인 예측이 아니라는 점을 짧게 안내해줘.
                """,
                tools = [
                    {
                        "type": "web_search"
                    }
                ],
                tool_choice = "required"
            )
            print(response.output_text or "운세 답변을 받지 못했습니다. 다시 요청해주세요.")

            # CLI에서도 API가 반환한 실제 출처 링크를 확인할 수 있게 표시합니다.
            sources = {}
            for item in response.output:
                if item.type == "message":
                    for content in item.content:
                        if content.type == "output_text":
                            for annotation in content.annotations:
                                if annotation.type == "url_citation":
                                    sources[annotation.url] = annotation.title
            if sources:
                print("\n[검색 출처]")
                for url, title in sources.items():
                    print(f"- {title}: {url}")
        except OpenAIError:
            print("API 요청에 실패했습니다. API 키, 사용 한도, 네트워크와 모델·웹 검색 도구 사용 권한을 확인해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n운세봇을 종료합니다.")
