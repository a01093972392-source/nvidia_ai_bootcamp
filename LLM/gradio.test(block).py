# interface : 간단한 테스트 환경 -> 버튼이 하나이고, 여러 component만 가지고 출력해보고...이런거만 해볼수 있다.
# blocks : 컴포넌트를 레고 블록처럼 끼워붙여서 구조나, 형태나 이런걸 좀더 자유롭게 꾸미고
#          여러 output을 생성하고, 특정 input에 대해 개별적인 함수를 구현하고...할수 있다.
# + Button을 만들수 있고, 엔터를 눌렀을 때 진행되는 행동 같은걸 만들 수 있다. 


import gradio as gr

def greet(name):
    return "안녕 " + name

def goodbye(name):
    return "잘가 " + name

with gr.Blocks() as demo:
    # 행 만들기
    with gr.Row():
        with gr.Column(scale=2):
            # 1번열
            # component를 순서대로 배치
            name = gr.Textbox(label="Name")
        with gr.Column(scale=1):
            # 2번열
            # 출력을 내보낼 컴포넌트도 따로 만들어준다.
            ouput = gr.Textbox(label="결과")
    with gr.Row():
        slider = gr.Slider(label="슬라이더")

    with gr.Row():
        # 행동을 지정하기 위하 버튼을 따로 만든다.
        button = gr.Button("run", variant='primary')


    # 버튼에 대한 행동을 지정
    button.click(
        fn = greet,                     # 버튼이 눌렸을 때 할 행동(함수)                                                                                
        inputs = name,                  # name이라는 textbox에 적힌 값을 가져가서 greet()함수에 매개변수로 전달.
        outputs = ouput                 # 이 함수가 return한 결과를 어느 컴포넌트에 뿌려줄거냐
    )
    # textbox쪽에서 enter를 눌렀을 때 하는 동작
    name.submit(
        fn = goodbye,
        inputs = name,
        outputs = ouput
    )
demo.launch()