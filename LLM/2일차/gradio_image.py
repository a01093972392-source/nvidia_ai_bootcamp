# Gradio에서 image 관련 component
import gradio as gr

def gray_scale(image):
    # 흑백으로 바꾸기
    image_gray = image.convert('L')
    return image_gray

def rotate_image(image):
    # image_rotated = image.rotate(90)
    # return image_rotated
    degrees = 0
    output = []
    while degrees < 360:
        output.append(image.rotate(degrees))
        degrees += 45
    return output


with gr.Blocks() as demo:
    with gr.Row():
        # 1번 열
        with gr.Column():
            input_img = gr.Image(type ='pil', height=300, width=300)
            btn = gr.Button("변환", variant='primary')


        # 2번 열
        with gr.Column():
            #gallery = gr.Image(type="pil", height=300, width=300)
            gallery = gr.Gallery(type='pil', columns=5)  # 여러 사진들을 걸을 수 있다.


    # 내가 버튼을 클릭했을 때
    btn.click(
        fn = rotate_image,
        inputs = input_img,
        outputs=gallery

    )
demo.launch()

