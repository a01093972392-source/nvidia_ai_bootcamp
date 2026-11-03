#산술 연산자
#연산자 우선순위: 수학과 동일
# a = 10
# b = 3

# print(a + b)
# print(a - b)
# print(a * b)
# print(a / b) # 나누기 소수점까지 나옴
# print(a // b) #몫
# print(a ** b) #제곱
# print(a % b) # 나머지

#비교 연산자
#우선순위 없음 앞에서부터 차례대로
# print(a > b)
# print(a < b)
# print(a == b)
# print(a != b)
# print(a >= b)
# print(a <= b)

#논리연산자
#&& || ! (and or not)
#연산자 우선순위: not > and > or
# print(True and True)
# print(True or False)
# print(False and False)
# print(False or False)
# print(not True)

#연산자 우선순위 
# 산술 연산 > 비교연산 > 논리연산

# ** 멤버쉽 연산
# 특정 요소가 어떠한 뭉텅이 안에 있는지를 확인하는 연산자
# 반복문에 사용

# sentence = "ai nvidia campus"

# print("ai " in sentence)

#1
# a, b = map(int, input().split())

# print("합: ", a + b)
# print("차 : ", a - b)
# print("곱 : ", a * b)
# print("몫 나누기 : ", a // b)
# print("나머지 나누기 : ", a % b)

#2
# a, b, c = map(int, input().split())
# sum = a+b+c
# avg = (a+b+c) /3 #나누기의 결과는 무조건 float
# #avg = round(avg, 2) # 소수점 두자리까지 반올림

# print(f"sum : {sum} , avg : {avg:.2f}") #formatting도 2자리수까지 반올림

#3
# a, b, c, d, e = map(int, input().split())

# power_ans = a**2 + b**2 + c**2 + d**2 + e**2
# print(power_ans % 10)

#4
# a, b = map(int, input().split())
 
# c = int((a + b) / 2) 
# d = int((a - b) / 2)
# print(c, d)

#5
# x1, y1 = map(int, input().split())
# x2, y2 = map(int, input().split())

# x_length = abs(x2 - x1)
# y_length = abs(y1 - y2)

# print(x_length + y_length)

#6
# a, b, x, y = map(int, input().split())

# #포털
# #a -> b로 가기
# a, b, x, y= map(int, input().split())
# s1 = abs(a - b) 
# #a -> x y -> b로 가기
# s2 = abs(a - x) + abs(y - b)
# s3 = abs(a - y) + abs(x - b)
# solution = min(s1, s2, s3)
# print(solution)  

#7
# X, Y, Z = map(int, input().split())
# # X = a + b + c
# # Y = a + b
# # Z = b + c
# print(Z - (X - Y))

#8
# N = int(input())

# day = N // 86400
# hour = (N % 86400) // 3600
# min = (N % 3600) // 60
# second = N % 60 

# print(f"{day}일 {hour}시간 {min}분 {second}초")

#9
# h, m = map(int, input().split())
# t = int(input())
# # 지나간 추가하기
# m += t
# # 얼마만큼 시간이 추가되느냐?
# h = (h + m // 60) % 24 
# # m을 60분 내의 분 체계로 변환
# m %= 60

# print(h, m)

#10
# N = int(input())

# first = N % 10
# second = (N // 10) % 10
# third = (N // 100)

# print(f"{first}{second}{third}")

#11
# a = int(input())
# b = int(input())

# a_3 = a % 10
# a_2 = (a // 10) % 10
# a_1 = (a // 100)

# b_3 = b % 10
# b_2 = (b // 10) % 10
# b_1 = (b // 100)

# print(a * b_3)
# print(a * b_2)
# print(a * b_1)
# print(a * b_3 + (a * b_2*10) + (a * b_1 * 100))
