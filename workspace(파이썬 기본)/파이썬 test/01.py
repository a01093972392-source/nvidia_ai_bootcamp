#CaptCha 코드
def solve(N, K, sample, passcode):
    '''
    N: sample의 길이 (5 <= N <= 300,000)
    K: passcode의 길이 (3 <= K <= N)
    sample: N 길이의 sample 
    passocde: K길이의 passcode
    '''
    sample_cur = 0
    passcode_cur = 0

    while sample_cur < len(sample) and passcode_cur < len(passcode):
        if sample[sample_cur] == passcode[passcode_cur]:
            passcode_cur += 1 
        sample_cur += 1

    return 1 if passcode_cur == len(passcode) else 0

        
    
        
        


#################################################

T = int(input())
for tc in range(1, T+1) :
    N, K = map(int, input().split())
    sample = list(map(int, input().split()))
    passcode = list(map(int, input().split()))
    solution = solve(N, K, sample, passcode)
    print(f"#{tc} {solution}")