#함수
#1. 매개변수 X, 반환값 X

# def greeting():
#     print("hello")

# #function calling 함수 호출
# greeting()

#2.매개변수 O, 반환값은 X
#매개변수(parameter -> machine learning에서도 많이 볼것)
#-> 우리가 함수를 사용할 때 전달할 재료

# def greeting2(count):
#     #내가 전달한 횟수만큼 인사를 하는 함수
#     for i in range(count):
#         print("hi")

# greeting2(5)  #5는 argument

#3. 매개변수 X, 반환 값 O
#쓸 일이 없는 함수
# def return_number():

#     return 1;
#     #1. 돌려준다
#     #2. 돌아간다(재귀적)

# a = return_number()
# print(a)

#4. 매개변수 O, 반환 값 O
#두개의 숫자를 전달받아서 합을 구하는 함수

# def add(a, b):
#     return a+b

# print(add(10, 15))


#함수 :function -> 코드 뭉텅이
#deff keyword를 사용
#함수명=> 소문자로 구성, 보통 명사형
#반환값을 지정하지 않아도, 파이썬에는 자동으로 None을 return

 
# def add(a,b):
#     return a + b


#1. default argument(parameter)
#매개변수에 직접 인자를 전달하지 않았을 때, 알아서 대입해줄 값을 설정
#default parameter는 필수로 전달해야하는 파라미터 뒤에 와야한다.

def multiply(a, b = 10):  #b에 10이라는 default값 설정
    return a * b

print(multiply(10))

def calculate(a, b, op = '+'):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
print(calculate(10, 8, '-'))
print(calculate(10, 8))


#2. *args
#함수에 무한대로 매개변수를 집어넣을 수 있게함.

def print_args(*args):
    for i in args:
        print(i, end = ' ')

print_args(1, 2, 3, 4, 5)
print()
print_args(1, 2, 3)

#3.**kwargs
#keyword arguments 위랑 똑같은 용도
#dictionary 지원

def print_kwargs(**kwargs):
    for k, v in kwargs.items():
        print(k,v)

print_kwargs(name='홍길동')


#type hinting(필수 x)
#함수를 작성하는 방식 -> 요즘 개발자 사이에서 많이 쓰임
#굳이 해야할 필요 X (인간이 이해하고 좀 더 쓰기 편하기 위함)

def subtract(a: int, b : int) -> int:
    return a - b

print(subtract(10, 8))
print(subtract({3, 4}, {4,  6}))