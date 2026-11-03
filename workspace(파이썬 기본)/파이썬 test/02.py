#답안지 채점

def solve(n, m, problem_ans, student_ans):
    '''
    n: 학생의 수 (3 <= n <= 30)
    m: 문제의 수 (2 <= m <= 40)
    problem_ans: m개의 문제에 대한 답안지 list
    student_ans: m개의 문제에 대한 n명의 제출 답안 list (2차원)
    '''
    # code here 
    score = 0
    score_li = []
    for j in range(n):
        score = 0 #초기화
        k = 1 #가산점
        for i in range(m):
            if (problem_ans[i] == student_ans[j][i]):
                score += k
                k += 1
            else:
                k = 1
        score_li.append(score)

    return max(score_li) - min(score_li)
                

"""
4
5 10
5 5 5 1 5 3 3 3 3 4
4 2 1 3 1 2 1 4 3 4
2 5 5 1 5 3 3 3 3 4
1 5 5 3 2 3 3 3 5 5
4 5 5 1 5 3 5 4 3 4
5 5 5 2 4 1 3 1 5 1
"""







###################################################################

T = int(input())
for tc in range(1, T+1):
    n, m = map(int, input().split())
    problem_ans = list(map(int, input().split()))
    student_ans = [list(map(int, input().split())) for _ in range(n)]
    solution = solve(n, m, problem_ans, student_ans)
    print(f"#{tc} {solution}")