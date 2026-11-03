#조건문
#주석
"""
이것도 주석입니다. 
아무것도 실행이 안됩니다.
"""

#만약 우리 점수가 60 점과 80점 사이라면 합격
#이렇게 쓰지 않기를 권장
# if 60 <= score <= 80:
#     print("합격")

# #권장 방법
# if (60 <= score) and (score <= 80):
#     print("합격")
# else:
#     printO("탈락")

#1
# K, N, M = map(int, input().split())

# if (M >= K * N):
#     print(0)
# else:
#     print(K * N - M)

#2
# a,b = map(int, input().split())
# max_num = max(a, b)
# min_num = min(a, b)
# dif = max_num - min_num
# print(dif)

#3
# a, b = map(int, input().split())

# if (a == b):
#     print(a + b)
# elif (a != b):
#     print(abs(a-b))

#4
# a, b = map(int, input().split())
# if (b % a == 0):
#     print("factor")
# elif (a % b == 0):
#     print("multiple")
# else:
#     print("neither")

#5
# W, V = map(int, input().split())

# if (W == 0) or (V == 1):
#     print("늦잠자기")
# else:
#     print("출근해야지")


#6
# A, B = map(int, input().split())
# if (A == B):
#     print("꿀꺽")
# else:
#     print("휴")

#7
# A, B = map(int, input().split())

# if (A == B):
#     print((A + B) *2)
# else:
#     print(A + B)

#8
# SA = 21
# N = int(input())

# if (N <= SA):
#     print(abs(N - SA))
# else:
#     print(2 * abs(N - SA))

#9
# a,b,c = map(int, input().split())

# if (a == b == c):
#     print("정삼각형")
# elif (a == b) or (b == c) or (c == a):
#     print("이등변 삼각형")
# else:
#     print("일반 삼각형")

#10
# CC = int(input())
# T = int(input())

# if (CC == 1) and (T > 20):
#     print("조용히 해!")
# elif (CC == 1) and (T < 7):
#     print("조용히 해!")
# else:
#     print("조용하군")

#11
# A, B = map(int, input().split())

# if (A + B == 10) or ((A == 10) or (B == 10)):
#     print("true")
# else:
#     print("false")

#12
# n = int(input())

# if ((90 <= n) and (n <= 110)) or ((190 <= n) and (n <= 210)):
#     print("Safe")
# else: 
#     print("Out")

#13
# m, w = map(int, input().split())

# if ((m >= 8) and (w > 2)) or ((m > 2) and (w >= 8)):
#     print(2)
# elif (m <= 2) or (w <= 2):
#     print(0)
# else:
#     print(1)

#14
# S, T = map(int, input().split())

# m = 5
# if (T == 1):
#     S -= m
#     if (S <= 60 + m):
#         print(0)
#     elif (61 + m <= S <= 80 + m):
#         print(1)
#     else:
#         print(2)
# elif (T == 0):
#     if (S <= 60):
#         print(0)
#     elif(61 <= S <= 80):
#         print(1)
#     else:
#         print(2)

#15
# N = int(input())

# if (N % 400 == 0):
#     print("Leap")
# elif (N % 4 == 0) and (N % 100 != 0):
#     print("Leap")
# else:
#     print("Normal")


#추가 문제 1
# n = int(input())

# if  (n > 10):
#     print(n)
#     print("10보다 크다")
# else:
#     print(n)

#추가 문제 2

