#문자열
#문자 + 열 -> 문자 여러 개가 결합되어있는 형태의 데이터
#파이썬에는 "문자"라는 데이터가 없음

# C++ : char(문자), string(문자열 형 데이터)

# print("hello")
# print(type("hello"))

# print("hi + bye")

# ###################################################

# #문자열의 정체성
# #1. iterable -> for문으로 요소 반복이 가능한 데이터
# a = "apple"
# for i in a:
#     print(i, end = ' ')

# #2. sequence -> index로 각각의 요소를 접근할 수 잇는 순서가 존재하는 데이터
# print(a[1]. a[-1],a[2:4])
# #3. immutable(불변) -> 요 하나의 요소는 "변수가 아니다" 


# b = "hello"
# # -> "bello"로 수정하고 싶다. 
# # c = list(b)
# # c[0] = 'b'
# # for i in range(len(c)):
# #     print(c[i], end='')

# b = "b" + b[1:]
# print(b)

######################################################
#1.문자열 변형 메소드(함수)
#-> 영문에만 적용되는 부분들이 많다.
# a = "baNaNa"
# #b = a.upper()
# print(a.upper())
# print(a.lower())
# print(a.capitalize()) #첫번째만 문자만 대문자로 변환

# print("nvidia ai campus".title()) #공백을 기준으로 처음 만나는 문자를 모두 대문자로 변환

# #2.문자열 검증 메소드(함수)
# b = "BANANA"
# print(b.isupper())  #대문자로 구성되어있으면 true, 아니면 false
# print(b.islower())
# print("abc123".isalpha()) #모든게 알파벣으로만 구성되어있으면 true, 아니면 false
# print("12345".isdigit()) #모든게 숫자로만 구성되어있으면 true, 아니면 false
# print("abc123".isalnum()) # alphbet + number 알파벳과 숫자로만 구성되어있으면 true, 아니면 false
# print("안녕".isalpha()) #한글도 일단 alpha() (숫자, 특수문자가 없다)라는 것을 판별 가능하다.and


# ########################################################
# #1. split()
# #map(int, input().split()) -> delimiter를 기준으로 문자열을 분해해서 리스트로 변환
# a = "nvidia ai campus" 
# b  = a.split()      #(아무것도 안넣으면) 알아서 공백을 기준으로 분리
# print(b)

# c = "hi, hello, my, name, is, pororo"
# d = c.split(',')
# print(d)


# #2. strip() : 파이썬의 native program을 가지고 뭔가를 만들고 입력을 받을 때 많이 쓰임
# #문자열의 앞뒤의 공백을 삭제해줌
# e = "                             hello                              "
# print(e)
# print(e.strip())
# print(e.rstrip()) #오른쪽에 존재하는 공백만 삭제
# print(e.lstrip()) #왼쪽에 존재하는 공백만 삭제



# #3. find()  : 문자열 내에 특정 문자열/문자가 존재하는 첫번째 index를 반환
# index = a.find('nvidia')
# print(index)

# print(a.find('ai'))  #없으면 -1
# #똑같이 동작하는 함수가 하나 있음 -> list에서 쓰던 index()

# print(a.index('ai')) #없으면 error 발생



# #4. join() 
# #리스트의 여러 요소들을 결합해서 하나의 문자열로 만드는 함수
# li = ['nvidia', 'ai', 'campus']
# new_str = '-'.join(li) #'리스트 내의 요소들을 결합할 기준".join(리스트)

# print(new_str)

#ASCII
#American Standard Code for Information Interchange
#키보드에서 표현할 수 있는 총 128개의 '기능' 및 '문자'를 8bit의 메모리에 저장해둔것.

# #1. ord() : 문자 -> 매핑된 숫자로 변환
# print(ord('0'), ord('a'), ord('A'))

# #A부터 Z까지 출력하는 프로그램
# #반복문
# for i in range(65, 65+ 26): #range(ord('A'), ord('Z') + 1)
#     print(chr(i))



#1

# s = input()

# for i in range(10):
#     print(s[0], end = '')

#2

# s1 = input()
# s2 = input()

# s3 = s1 + s2
# print(s3[::-1])

#3

# s = input()
# result = ""
# for i in range(len(s)):
#     if ((i+1) % 2 != 0):
#         result = result + s[i]
#     else:
#         continue
# print(result)

#4

# s = input()

# st = s.split()
# for i in range(len(st)):
#     print(f"{i+1}.", f"{st[i]}")

#5

# email = input()
# id_domain = email.split('@')
# print(f"ID:", id_domain[0])
# id_domain_result = id_domain[1]
# domain = id_domain_result.split('.')
# print(f"Domain:", domain[0])


#6

# s = input()
# for i in range(len(s)):
#     print(s[i] + s[i], end = '')

#7

# s = input()

# for i in range(len(s)+1):
#     print(s[0:i], end = '')

#8

# form = input()
# li = form.split('+')

# print(int(li[0]) + int(li[1]))

#9

# s = input()
# li = s.split()

# li_re = li[::-1][0:2]
# li_re_result = []

# for i in range(len(li_re)):
#     li_re_result.append(li_re[i])

# result = li_re_result[::-1]
# for j in range(len(result)):
#     print(result[j], end = ' ')


#10
# n, k = map(int, input().split())
# s = input()

# lower_case = s[k-1:]
# S = str(s[0:k-1]) + lower_case.lower()
# print(S)    

#11

# s = input().lower()

# if (s[::-1] == s):
#     print(1)
# else:
#     print(0)


#12

# jelly = input().lower()
# jelly_sort = sorted(jelly)

# for i in range(len(jelly_sort)):
#     print(jelly_sort[i], end='')

#13

# day = input()

# d = day.split('.')

# print(f"{d[2]}", f"{d[1]}", f"{d[0]}", sep='-')

#14

# date = input()
# d = date.split('.')

# if (len(d[1]) == 1):
#     d[1]= "0" + d[1]
 
# if(len(d[2]) == 1):
#     d[2]= "0" + d[2]

# result = [] 
# result.append(d[0][2:4])
# result.append(d[1])
# result.append(d[2])

# day = result[0] + result[1] + result[2]
# print(day, "XXXXXXX", sep='-')

#15
# n = input()

# next = ord(n) + 1
# print(chr(next))


#16
#S = "ab1c9d7jeden"

# S = input()

# # 숫자만 추출
# # 문자열 검증 함수 digit()을 활용해서 문자가 숫자인지 확인
# ret = 0
# cur = 0
# for i in S:
#     if i.isdigit():
#         #i는 숫자다 -> cur에서 뒤에 자릿수를 하나 넘겨주고 -> 지금 i를 더해준다.
#         cur = cur * 10 + int(i)
#     else: #i는 숫자가 아니다 -> 이전까지 숫자가 존재했다면 
#         ret += cur #정답에 누적
#         cur = 0 #다음 숫자가 나열할 수 있도록 초기화
#     #만약 우리의 cur이라는 숫자가 4자릿수 이상이 되면
#     if cur > 999:
#         ret += cur
#         cur = 0
# ret += cur  #숫자로 끝나는것을 방지
# print(ret)


#17

# S = input()
# key = int(input())
# #모든 문자열을 주어진 키대로 밀어준다.
# ret = "" #여기다가 변환된 문자를 하나씩 더해서 새로운 메시지를 만들자.
# for i in S:
#     #예외처리 1: 만약 스페이스 (공백)이라면 ->아무것도 안해야 함
#     if i == ' ':
#         ret += i  #스페이스를 넣어줌
#         continue
#     #i = 각각의 문자
#     #1. 일단 숫자로 문자를 변환
#     #2. key만큼 더해줌
#     #3. 다시 문자로 변환

#     #예외처리 2: 만약 key를 더했을 때 ord('z')인 122를 넘어가면 -> 거기서 26을 뺀다  
#     # ret += chr(((ord(i) - ord('a') + key) % 26) + ord('a')) -> 더 현명한 방법!
    
#     new_ascii = ord(i) + key
#     if new_ascii > ord('z'):
#         new_ascii = new_ascii - 26

#     new_char = chr(new_ascii)
#     ret += new_char
# print(ret)


