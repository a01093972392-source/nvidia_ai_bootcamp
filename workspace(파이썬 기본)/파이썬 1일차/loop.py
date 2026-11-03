#for 문
#1. 횟수적 반복
#hello를 10번 출력

# for i in range(10):
#     print(i, "hello")

# for i in range(1, 11, 2):
#     print(i)

#10부터 1까지 출력(역순이면 end + 1까지)
# for i in range(10, 0, -1):
#     print(i, end = ' ')

#n을 입력받고 1 ~ n까지 3의 배수만 출력

# n = int(input())

# for i in range(1, n+1):
#     if (i % 3 == 0):
#         print(i, end = ' ')
        

#while 문

# n = 0 
# while n < 10:
#     print(n, end= ' ')
#     n += 1

#10부터 1까지 출력

# n = 10
# while n > 0:
#     print(n, end = ' ')
#     n -= 1

#n을 입력받고 3의 배수만 출력

# n = int(input())

# i = 1
# while i <= n:
#     if (i % 3 == 0):
#     my_input = int(input())
#     sum += my_input
# print(sum)

#break
# for i in range(10):
#     if (i == 5):
#         break
#     print(i, end = ' ')
# print('이건 무조건 실행')

# i = 0
# while i < 10:
#     if (i == 5):
#         break
#     print(i, end = ' ')
#     i += 1

# continue
# for i in range(10):
#     if (i == 5):
#         continue
#     print(i, end = ' ')

# i = 0
# while i < 10:
#     i += 1
#     if (i == 5):
#         continue
    
#     print(i-1, end = ' ')



#1
# k, n = map(int, input().split())

# for i in range(k, k+n):
#     print(k, end=' ')
#     k = k + 3

#2
# n = int(input())

# #조회수 
# j = 1
# for i in range(1, 1000000):
#     j = j * i
#     if (n <= j):
#         print(j)
#         break


    
#3

# N = int(input())
# i = 1

# sum_ju = 0
# sum_ja = 0

# while i <= N:
#     ju, ja = map(int, input().split())
#     if (ju == ja):
#         sum_ju += ju
#         sum_ja += ja
#     elif (max(ju, ja) == ju):
#         sum_ju = sum_ju + ju + ja
#     elif (max(ju, ja) == ja):
#         sum_ja = sum_ja + ju + ja
#     i += 1

# print(sum_ju, sum_ja, sep='\n')

#4 
# N = int(input())
# sum = 0
# for i in range(0, len(str(N)), 2):
#     sum += int((str(N)[i : i+2]))
# print(sum)

#반복문과 연산자만 사용해서 하기!
# N = int(input())
# sum = 0
# while N > 0:
#     sum += N % 100
#     N = N // 100
# print(sum) 


#5

# N = int(input())

# for i in range(1, N+1):
#     if (i % 3 == 0) and (i % 5 != 0):
#         print("Fizz")
#     elif (i % 5 == 0) and (i % 3 != 0):
#         print("Buzz")
#     elif (i % 3 == 0) and (i % 5 == 0):
#         print("Fizz Buzz")
#     else:
#         print(i)

#6

# N = int(input())
# even = 0
# odd = 0 
# for i in range(1, N+1):
#     if (i % 2 == 0):
#         even -= i
#     elif (i % 2 != 0):
#         odd += i

# print(even + odd)

#7
# n = int(input())

# for i in range(1, n+1):
#     if (n % i == 0):
#         print(i, end=' ')

#8
# N = int(input())

# sum = 0
# while N > 0:
#     sum += N % 10
#     N = N // 10
# print(sum)

#9

# max_mem = 0
# step_mem = 0
# total_mem = 0
# i = 1
# while i <= 4:
#     gf, go = map(int, input().split())
#     step_mem = go - gf
#     total_mem += step_mem
#     if (total_mem > max_mem):
#         max_mem = total_mem
#     i += 1

# print(max_mem)


#10

# x, y, N = map(int, input().split())
# #횟수
# count = 0
# while x <= N and y <= N:
#     count += 1
#     #방법
#     if x < y:
#         x += y
#     else:
#         y += x
# print(count)

#11

# N = int(input())

# N_digit = []
# while N > 0:
#     N_digit.append(N % 2) 
#     N =  N // 2
# # print(N_digit, len(N_digit))

# for i in range(1, len(N_digit)+1):
#     print(N_digit[-i], end='')

# N = int(input())

# pos = 1 #처음에는 1의 자리수에 곱한다.and
# ret = 0
# while N > 0:
#     ret += (N%2) * pos
#     N //= 2
#     pos *= 10
# print(ret)
    
