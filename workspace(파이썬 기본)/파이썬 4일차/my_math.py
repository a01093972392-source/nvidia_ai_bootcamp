#나의 모듈
#4개의 함수
#add, subtract, multiply, divide
#모든 함수는 2개의 매개변수를 받고, return 값이 있어야 하며,
#*divide의 경우에는 만약 0으로 나눌려고 한다면, "Error"라는 문구를 return 

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

# def divide(a, b):
#     if b == 0:
#         return "Error"
#     else:
#         return a / b

#try, except 문 (error handling) -> if 문으로 해결이 가능
#error가 발생했을 때 뭘해야 하는지

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 'Error, 0으로 나눌 수 없습니다.'
    except TypeError:
        return 'Error, 타입이 맞지 않습니다.'
        

#매직메소드 
#namespace가 main일 때
if __name__ == "__main__":
    #unit test
    print(divide(1, 0))
    print(divide(10,20))
    print(40,30)
    a = 1 
    print(a.__add__(3))
    print(divide(10, hi))

