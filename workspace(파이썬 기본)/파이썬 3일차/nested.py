#중첩 반복문
#반복문 안에 반복문이 돌아가는 구조(nested loop)

# for i in range(5):
#     for j in range(3):
#         print(j, end = ' ')
#     print()


#중첩 리스트

# li = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7,  8, 9]
# ]

# print(li[0][1])
# print(li[0][1:])


# #n차원 리스트의 요소를 모두 볼려면 결국 n차원 반복문이 필요
# for i in li:
#     for j in i:
#         print(j, end = ' ')
#     print()
# #indexing / len 으로도 접근
# print()
# for i in range(len(li)):
#     for j in range(len(li[i])):
#         print(li[i][j], end = ' ')
#     print()


#list comprehension
#말 그대로 list를 잘 이해하고 있냐?
#리스트를 빠르게 초기화할 수 있는 방법

#비어있는 리스트 만들기
#li = []

#0으로 초기화되어있는 길이 5짜리 리스트
#li2 = [0] * 5

#길이가 n일때 0부터 n-1까지로 초기화된 리스트
# li3 = []
# #n=5일때
# for i in range(5):
#     li3.append(i)

# li4 = [i for i in range(5)]
# print(li3, li4)


# li5 = [0 for _ in range(10)]
# print(li5)

# li6 = [[] for _ in range(5)]
# print(li6)

#####################################
#2차원 리스트를 초기화 할 때.

#[[1,2,3], [1,2,3], [1,2,3]]
# li7 = []
# for i in range(3):
#     li7.append([1,2,3])
# print(li7)

# li8 = [[1,2,3] for i in range(3)]
# li9 = [[j for j in range(1, 4)] for i in range(3)]
# li = []
# for i in range(3):
#     x = []
#     for j in range(1, 4):
#         x.append(j)
#     li.append(x)


#1

# N = int(input())
# result = 0

# for i in range(1, 7):
#     for j in range(1, 7):
#         if (i + j == N):
#             result += 1
#         else:
#             continue
# print(result)


#2 

#N * N 크기 도화지, M번 칠하기
# n, m = map(int, input().split())

# li = [[0 for _ in range(n)] for i in range(n)]


# for i in range(m):
#     y, x = map(int, input().split())
#     for j in range(3):
#         li[y-1][x-1+j] = 1
#     for k in range(3):
#         li[y][x-1+k] = 1
#     for q in range(3):
#         li[y+1][x-1+q] = 1

# for s in range(len(li)):
#     for t in range(len(li[s])):
#         print(li[s][t], end=' ')
#     print()


#3

#n(행) * m(열) 행렬
# n, m = map(int, input().split())

# A = []
# B = []
# for _ in range(n):
#     A.append(input().split())
# for _ in range(n):
#     B.append(input().split())


# for l in range(len(A)):
#     for u in range(len(A[l])):
#         print(int(A[l][u]) + int(B[l][u]) , end = ' ')
#     print()


#4
# li = []
# for _ in range(9):
#     li.append(input().split())

# max_num = -1
# row = 0
# col = 0
# for i in range(len(li)):
#     for j in range(len(li[i])):
#         if (int(li[i][j]) > max_num):
#             max_num = int(li[i][j])
#             row = i+1
#             col = j+1
# if max_num == 0:
#     row = 1
#     col = 1

# print(max_num)
# print(row, col, end = ' ')


#5
#마스크 개수
# n = int(input())

# paper = [[0] * 100 for _ in range(100)]
# cnt = 0

# for _ in range(n):
#     x, y = map(int, input().split())
#     for i in range(x, x+10):
#         for j in range(y, y+10):
#             if paper[i][j] == 1:
#                 continue
#             paper[i][j] = 1
#             cnt += 1
        
# # sum = 0
# # for k in range(len(paper)):
# #     for q in range(len(paper[k])):
# #         if (paper[k][q] == 1):
# #             sum +=1 
# #         else: 
# #             continue
# print(cnt)


#6

# n = int(input())
# # 1000 * 1000 모눈종이 (0으로 초기화)
# paper = [[0] * 1000 for _ in range(1000)]

# # 1. 색종이를 순서대로 도화지에 올립니다 (1번부터 n번까지)
# for paper_id in range(1, n + 1):
#     x, y, w, h = map(int, input().split())
    
#     # 가로 x부터 x+w까지, 세로 y부터 y+h까지 해당 색종이의 번호로 덮어씁니다.
#     for i in range(x, x + w):
#         for j in range(y, y + h):
#             paper[i][j] = paper_id

# # 2. 각 색종이의 노출 면적을 저장할 리스트 (인덱스 1부터 n까지 사용)
# cnt_list = [0] * (n + 1)

# # 3. 전체 도화지를 한 번만 순회하여 어떤 색종이가 덮이지 않고 맨 위에 있는지 카운트합니다.
# for i in range(1000):
#     for j in range(1000):
#         if paper[i][j] > 0:
#             cnt_list[paper[i][j]] += 1

# # 4. 1번 색종이부터 차례대로 최종 노출 면적을 출력합니다.
# for k in range(1, n + 1):
#     print(cnt_list[k])


#7

# n = int(input())

# for i in range(1, n+1):
#     num_str = str(i)
#     num_str_cnt = num_str.count('3') + num_str.count('6') + num_str.count('9')

#     if num_str_cnt > 0:
#         print("-" * num_str_cnt, end = ' ')
#     else:
#         print(i, end = ' ')


#8 

# n = int(input())

# arr = []
# for i in range(1, n +1):
#     arr.append([i for _ in range(n)])

# for j in range(len(arr)):
#     for k in range(len(arr[j])):
#         print(arr[j][k], end = ' ')
#     print()

#9

# n = int(input())

# arr = [list(range(1, n+1)) for _ in range(n)]
        
# for i in range(len(arr)):
#     if i % 2 != 0:
#         for j in range(len(arr[i])-1, -1, -1):
#             print(arr[i][j], end = ' ')
#     else:
#         for j in range(len(arr[i])):
#             print(arr[i][j], end = ' ')
    
#     print()


