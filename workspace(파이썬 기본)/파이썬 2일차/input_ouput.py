#입력과 출력

# 출력
# print(내용)
# print("문자열")
# print("hello world")

# # 입력
# # input()

# a = input()
# print(a)

#도전: 이름을 입력받기
#안녕? <이름> 오늘도 힘내자.a
#print()문은 각각 모두 맨 끝에 '줄바꿈이 추가된다'
#\n(enter) -> escape 문자 -> 키보드에 있는데, 문자로 표현하지 못하는것

# name = input("이름을 입력하세요")
# print("안녕?" ,end = '')
# print(name, end = '')
# print("오늘도 힘내보자", end = '')

# a = "사과"
# b = "바나나"

# escape 문자
# 항상 쓰는 것: \n (줄바꿈)
# 쓸 수 있는 것 : \t (4칸 space), \b (backspace)

# sep : print문 안의 쉼표의 역할을 바꾼다
# print(a, b, sep='--')

#f-string formatting이라는 아주 좋은 출력 방식이 있음

# print(f"안녕?, {name}, 만나서 반가워, 너는 {a}를 좋아하니?")

#마지막 출력 도전
#연도를 입력받고, 10년 후의 연도를 출력하는 프로그램을 만들기
#금년은 2026년이예요, 10년뒤면 2036년이겠네요

# year = int(input("올해년도를 입력해주세요"))
# print(type(year))
# print(f"금년은 {year}년이예요, 10년뒤면 {year+10}이겠네요")
# print("C:\\Users\\PC\\Downloads")1
# print("hello\\nworld")

# A, B = map(int, input().split())
# print(A + B)

# a = input()
# b = input()
# c = input()

# print(a, b, c, sep='~')

# a = input()
# b = input()

# print(a, end = '!')
# print(b)


#escape를 활용하여 문자열 안에 문자 넣기
# print("\'Hello'")
# print('\"World"')

# a = 10
# b = 20
# print(f"{a} + {b} = {a+b}")
# a = 30
# b = 40
# print(f"{a} + {b} = {a+b}")


# age = int(input())

# print(f"I am {age} years old")


# n = int(input())

# n1 = n + 10
# n2 = n1 - 5
# n3 = n2 * 2
# n4 = n3 // 3
# print(n1, n2, n3, n4, end = ' ')