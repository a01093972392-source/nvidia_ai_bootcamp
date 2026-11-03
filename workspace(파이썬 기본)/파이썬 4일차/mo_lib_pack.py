#라이브러리/모듈 임포팅 방법
# import my_math

# #my_math 안에 정의된 add라는 함수를 사용
# print(my_math.add(10, 20))

# print(my_math.divide(20, 0))

#라이브러리 내에서 필요한 기능만 가져올 수도 있음
# from my_math import divide, add

#주의 사항: 이 안에 divide()라는게 있다면 충돌날 수 있음.
# print(divide(1, 2))

#라이브러리 내에 모든 이름들을 내 파일에 집어넣을 수 있음.(권장 방식은 아님)
#from my_math import *


#name aliasing -> 우리가 라이브러리 이름을 바꿔서 쓸 수 있음.abs
# import my_math as mm

# print(mm.add(3, 5))

#어떤 에러들이 있는지

#NameError: 없는 이름을 호출

#TyepError: 연산을 하는데 있어 인자들의 타입이 맞지 않음

#ValueError: 함수를 호출할 때 인자의 타입이 맞지 않는 경우

#IndexError: 리스트에 없는 index를 접근하려고 했을 때

#keyError: 딕셔너리에 존재하지 않는 key를 접근하려고 할 때 

#SyntaxError: 문법 에러

#semantic Error: 인간 에러-> 로직이 잘못됨

#################################################################
import random as rd

#난수 생성
#randint(st, ed): st부터 en(포함)까지 숫자 중 랜덤한 숫자를 하나 반환
# for i in range(10): 
#     print(rd.randint(1, 6))

# #random()
# print(rd.random())

# #list에 활용할 수 있는 랜덤 명령어들
# li = [1, 2, 3, 4, 5]

# #li를 섞을 수 있음.
# rd.shuffle(li)  #in-place함수 (li자체에 변화를 주는 것, 반환이 없음)

# #리스트 내에서 랜덤으로 뽑아오기
# card = rd.choice(li)
# print(card)
# print(li)

# #여러 개 뽑아오기
# cards = rd.choices(li, k = 3)  #k값의 default는 1
# print(cards)

#여러 개 뽑아올 때 각 인자의 weight를 설정

# cards = rd.choices(li, k = 3, weights = [90, 20, 1, 1, 1])
# print(cards)

# import time, os
# delay 같은것을 시킬 수 있음

# for i in range(10):
#     print(i, end = ' ')
#     time.sleep(1)  # ROS에서도 많이 사용
#     os.system('cls')  #linux: clear


#시간과 날짜
#import datetime

from datetime import datetime

now = datetime.now()
print(type(now))

# %Y:연도 , %m: 월, %d:날짜
print(now.strftime("%Y년 %m월 %d일"))
print(now.strftime("Y년 %m월 %d일 %H시 %M분"))

