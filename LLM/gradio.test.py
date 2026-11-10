# Gradio 
# 간단하게 몇줄의 파이썬 코드로 "배포 가능한" UI(interface)를 만들 수 있게 해주는 라이브러리

# 1. interface: 단순한 테스트 환경
# 2. blocks : 조금 더 어렵지만 -> 조금 더 실용적인 배치나 더 많은 컴포넌트를 쓸 수 있다. 
import gradio as gr


def greet(name, age, gender, hobbies, tired, lang, file):
    result = " "
    result += f"이름 : {name}\n"
    result += f"나이 : {age}\n"
    result += f"성별 : {gender}\n"

    # hobbies (checkbox)로 부터 전달될 때 list의 형태로 들어온다.
    result += "취미 : "
    for h in hobbies:
        result += h + " "
    result += '\n'
    result += f"나의 피로도 : {tired}\n"
    result += f"나의 최애 언어 : {lang}\n"
    # 파일
    result += str(open(file, 'r', encoding='utf8').read())
    return result

demo = gr.Interface(
    fn = greet,                                                                  # interface환경에서는 "submit" 버튼을 눌렀을 때 할 행동
    inputs = [                        
        gr.Textbox(label="이름"),                                                 # Textbox = 입력창            -> 1번째 매개변수(인자)
        gr.Number(label="나이", minimum=1, maximum=99),                           # 숫자만 입력할 수 있는 입력창   -> 2번재 매개변수(인자)
        gr.Radio(label="성별", choices=['남', '녀']),                              # 한개 항목만 선택가능한 라디오버튼 -> 3번째 매개변수(인자)
        gr.CheckboxGroup(label="취미", choices = ["게임", "독서", "축구", "공부"]),  #여러개가 중복 선택 가능한 체크박스 -> 4번째 매개변수(인자)
        gr.Slider(label="피로도", minimum=0, maximum=100),                         # 5번째 매개변수(인자)
        gr.Dropdown(label="언어", choices=['python', 'C++', 'Linux']),             # 6번째 매개변수(인자)
        gr.File(label="파일", type='filepath')                                     # 7번째 매개변수(인자)
    ],                                    
    outputs= gr.Textbox(label="출력")
)

# 프로그래밍 launching
demo.launch()           # To create a public link, set `share=True` in `launch()



# blocks

import gradio as gr

with gr.Blocks() as demo:
    # component를 순서대로 배치
    name = gr.Textbox(label="Name")
    # 출력을 내보낼 컴포넌트도 따로 만들어준다.
    ouput = gr.Textbox(label="결과")

demo.launch()