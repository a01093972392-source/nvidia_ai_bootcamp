#리스트
# li = [] -> 비어있는 리스트 생성

# li = [1, 2, 3, "hello", True]
# print(li)

# #각 요소에 접근하기 - indexing
# #각 요소 - index
# print(li[4])
# li[4] = "ai campus"
# print(li[4])

#리스트: iterable
#sequence 데이터: 순서를 가지는 데이터(index가 존재)
#mutabel 데이터: 요소들의 변화를 줄 수 있는 데이터
#반복문 
# for i in li:
#     print(i)

# # 반복문 - index적 접근
# # len() = built-in function -> iterable의 길이 -> 요소들의 개수
# for i in range(len(li)):
#     print(li[i])

# 음수 indexing도 가능
# print(li[-2])

#list 연산자
# + : 리스트1 + 리스트2 = 리스트1의 뒤에 리스트2가 붙음
# * : 리스트를 n번 반복

# li = li + ['xyz']
# print(li)

# slicing
# 리스트의 일부분만 잘라내는 것
# list[start:end] => start 인덱스부터 end-1 인덱스까지의 서브 리스트를 반환

# print(li[1:4])
# # list[start:end:step]
# print(li[1:4:2])
# # start -> 무조건 처음(0)
# # end -> 무조건 마지막(len(li) - 1)

# # 외우면 좋을 것 -> slicing 을 통해 뒤집을 수 있음
# print(li[::-1])


# # copy
# li1 = [1, 2, 3]
# li2 = li1
# print(li1, li2)
# li[1] = 99
# print(li1, li2)

# = 으로 복사하면 위의 문제가 생김
# 개별적인 메모리를 가지는 새로운 리스트로 연결을 시켜줘야 한다.
# shallow copy -> 1차원 리스트에서만 적용

# li2 = li1[:]
# print(li1, li2)
# li2[0] = 0
# print(li1, li2)


#deep copy: 깊은 복사
#리스트 안에 리스트가 존재하는 그런 '중첩 배열' 
# import copy

# li3 = [1, [1, 2 , 3], 2]
# li4 = copy.deepcopy(li3)
# li3[0] = 0 
# print(li3, li4)
# li3[1][1] = 99
# print(li3, li4)


#리스트를 활용하기 위해 리스트에서만 쓸 수 있는 고유 함수
# li = []

# #1. list에 요소를 추가
# # append(요소)
# li.append(1)
# li.append(2)
# li.append(3)
# print(li)

#2. 중간 삽입 - 쓸일이 없음
# insert(index, 요소)
# li.insert(1, 4)
# print(li)

# #3. index(요소):요소의 index 찾기 -웬만해서 쓸일이 없음
# print(li.index(4))
# li.append(1)
# print(li.index(1)) #같은게 여러개가 있다면 -> 무조건 앞에 있는것을 가져옴

# #4. 삭제의 기본: pop()
# # 리스트의 맨 뒤의 요소를 삭제
# # return : 맨 뒤의 요소
# li.pop()
# print(li)

# pop(index) : index의 요소를 삭제
# li.pop(1)

# # remove(요소) : 요소를 삭제
# li.append(1)
# li.remove(1)


# #정렬
# li5 = [3, 8, 9, 7, 1, 2]
# #in-place method(funcition)
# li5.sort()  #숫자만 있어야함
# #뒤집기
# li5.reverse() # li5[::-1]


# #built-in function
# print(max(li5)) #문자열 있으면 불가
# print(min(li5)) #문자열 있으면 불가
# print(len(li5)) #문자열 있어도 가능
# print(sum(li5)) #문자열 있으면 불가






#1
# n = int(input())
# even = 0
# a = list(map(int, input().split()))

# for i in range(0, len(a)):
#     if (a[i] % 2 == 0):
#         even += 1
    
# print(even)


#2
# n = int(input())
# li = list(map(int, input().split()))

# # print(li)
# li.sort()
# li.pop(0)
# li.pop(-1)

# # print(li)

# # print(len(li))
# sum = 0
# for i in range(len(li)):
#     sum += li[i]

# print(sum // (n-2))


#3
# n = int(input())
# li = list(map(int, input().split()))
# sum = 0
# for i in range(len(li)):
#     sum += li[i]
#     if (li[i] == 13) and (i < len(li) - 1):
#         sum = sum - li[i] - li[i + 1]
#     elif (li[i] == 13) and (i >= len(li) - 1):
#         sum = sum - li[i]

# print(sum)

#4
# n = int(input())
# li = list(map(int, input().split()))

# print(li)

# found = "false"
# for i in range(len(li)):
#     # print(li[i])    
#     if (i < len(li) - 2):
#         if (li[i] % 2 == 0) and (li[i+1] % 2 == 0) and (li[i+2] % 2 == 0):
#             found = "true"
#             break
#     elif (i < len(li) - 2):
#         if (li[i] % 2 != 0) and (li[i+1] % 2 != 0) and (li[i+2] % 2 != 0):
#             found = "true"
#             break
# print(found)


# found = "false"
# for i in range(1, len(li) - 1):
#     if (li[i-1] % 2 == 0) and (li[i] % 2 == 0) and (li[i+1] % 2 == 0):
#         found = "true"
#         break
#     elif (li[i-1] % 2 != 0) and (li[i] % 2 != 0) and (li[i+1] % 2 != 0):
#         found = "true"
#         break
    
# print(found)


#5
# n = int(input())
# li = list(map(int, input().split()))

# check = "false"
# for i in range(len(li)):
#     if (li[0] == li[-1]) or (len(li) == 1):
#         check = "true"
#     else:
#         check = "false"

# print(check)

#6

# n = int(input())
# li = list(map(int, input().split()))

# for i in range(len(li) - 1):
#     temp = li[i]
#     li[i] = li[i+1]
#     li[i+1] = temp

# for j in range(len(li)):
#     print(li[j], end = ' ')


#7
# n = input()
# arr = list(map(int, input().split()))
# dif = []
# for i in range(1, len(arr)):
#   dif.append(abs(arr[i] - arr[i-1]))
# for j in range(len(dif)):
#   print(dif[j], end = ' ')


#8
# n = int(input())
# li = []

# i = 0
# factor = ""
# while i < n:
#   factor = input()
#   li.append(factor)
#   i += 1
# li2 = li[::-1]
# for j in range(len(li2)):
#   print(li2[j])


#9

# N, K = map(int, input().split())

# arr = []
# li = list(map(int, input().split()))
# for i in range(len(li)):
#     arr = li[-1:-(K+1):-1]

# for j in range(1, len(arr) + 1):
#   print(arr[-j], end = ' ')


#10

# N = int(input())
# li = list(map(int, input().split()))
# M = int(input())

# multiple = []
# divide = []
# sum_m = 0
# sum_d = 0
# for i in range(len(li)):
#   if (M % li[i] == 0) and (li[i] % M != 0):
#     divide.append(li[i])
#   elif (li[i] % M == 0) and (M % li[i] != 0):
#     multiple.append(li[i])
#   elif (M % li[i] == 0) and (li[i] % M == 0):
#     multiple.append(li[i])
#     divide.append(li[i])
# for j in range(len(multiple)):
#   sum_m += multiple[j]
# for k in range(len(divide)):
#   sum_d += divide[k]

# print(sum_d, sum_m, sep='\n')

#11

# li = list(map(int, input().split()))
# even = []
# odd = []
# default = 1
# for i in range(len(li)):
#   if (li[i] % 2 == 0):
#     even.append(li[i])
#   elif (li[i] % 2 != 0):
#     odd.append(li[i])
#   else:
#     default

# max_even = 0
# max_odd = 0
# for j in range(len(even)):
#   if (even[j] > max_even):
#     max_even = even[j]

# for k in range(len(odd)):
#   if (odd[k] > max_odd):
#     max_odd = odd[k]

# print(max_even + max_odd)


#12

#구간의 수
# N = int(input())

# #구간마다의 높이 정보 저장
# arr = []
# #구간마다의 차이
# dif = []

# #오르막 여부
# check_height = []
# #최대 오르막길
# max_height = 0

# #구간마다의 높이 정보
# for i in (range(N)):
#   height = int(input())
#   arr.append(height)

# for j in range(0, len(arr)):
#   dif.append(arr[j] - arr[j-1])

# for k in range(1, len(dif)):
#   if (dif[k] > max_height):
#     max_height = dif[k]
#     check_height= [k ,k+1]


# # print(len(check_height))
# if (len(check_height) == 0):
#       print(0)
# for q in range(len(check_height)):
#   print(check_height[q], end = ' ')

#13

# arr = []
# for i in range(1, 21):
#     arr.append(i)

# for j in range(10):
#     lb, ub = map(int, input().split())
#     # lb-1부터 ub까지의 구간을 슬라이싱한 후 뒤집어서 다시 대입
#     arr[lb-1:ub] = arr[lb-1:ub][::-1]

# for k in range(len(arr)):
#     print(arr[k], end=' ')