def solve(N, board):
    '''
    N: 게임판의 한 변의 크기 (3 <= N <= 50)
    board: N x N 크기의 게임판에 대한 정보
    '''
    # code here
    for i in range(N):
        for j in range(N):
            if (board[i][j] == board):
                pass


T = int(input())
for tc in range(1, T+1) :
    N = int(input())
    board = [list(map(int, input().split())) for _ in range(N)]
    solution = solve(N, board)
    print(f"#{tc} {solution}")