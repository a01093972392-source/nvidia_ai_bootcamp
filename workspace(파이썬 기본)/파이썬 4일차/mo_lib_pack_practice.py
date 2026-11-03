#모듈 실습
#1 (숫자 UP, DOWN)
import random as rd

# num = rd.randint(1, 100)
# cnt = 1

# while True:
    
#     guess = int(input(">> 추측값을 입력하세요: "))
#     if (num > guess):
#         print("UP")
#         cnt += 1
#     elif (num < guess):
#         print("DOWN")
#         cnt += 1

#     else:
#         print(f"총 {cnt}번만에 맞추셨습니다!")
#         break


#2 (짝 맞추기 게임)
# li = []
# for i in range(2):
#     for j in range(1, 11):
#         li.append(j)


# rd.shuffle(li)
# cnt = 1

# while len(li) != 0:
#     print("[X]" * len(li))
#     id_1, id_2 = map(int, input("index 두 개를 한 줄에 띄워서 입력하세요:  ").split())
    
#     if (id_2 > len(li)) or (id_1 > len(li)):
#         print("적절한 값을 입력하세요")
#         continue
#     if (li[id_1] == li[id_2]):
#         print("<<<<<<<<<<<<MATCH!>>>>>>>>>>>>>>>>")
#         print(li[id_1], li[id_2], sep=' : ')
#         li.pop(li.index(id_1)) 
#         li.pop(li.index(id_2))
#         cnt += 1
#     else:
#         print(li[id_1], li[id_2], sep=' : ')
#         continue
#         cnt += 1  

# print(cnt)
    

#3.카드 게임

shape = ["◆", "♣", "♥", "♠"]
ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] 
suit = []

for i in shape:
    for j in ranks:
        suit.append(str(j) + i)

rd.shuffle(suit)


com = []
user = []

for i in range(2):
    com.append(suit.pop(0))
for j in range(2):
    user.append(suit.pop(0))

#  print(com, user, end = ' ')

#화면 출력
def display(a):
    if (a == 0):
        print("[COM]: ", [com[0], '[X]'])
        print("[USER]: ", user)
    elif (a == 1):
        print("[COM]: ", com)
        print("[USER]: ", user)

#점수 계산
def calculate(li):
    total = 0
    aces = 0 

    for card in li:
        rank = card[:-1] 

        if rank in ['J', 'Q', 'K']:
            total += 10
        elif rank == 'A':
            total += 11
            aces += 1
        else:
            total += int(rank)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

total_com_sum = 0
total_user_sum = 0
button =  1
while button == 1:
    display(0)
    if (calculate(user) > 21):
        total_com_sum = calculate(com)
        total_user_sum = calculate(user)
        print(f"COM : {total_com_sum} VS USER : {total_user_sum}")
        print("======= DEALER WINS =======")
        break
    elif (calculate(com) > 21):
        diplay(1)
        total_com_sum = calculate(com)
        total_user_sum = calculate(user)
        print(f"COM : {total_com_sum} VS USER : {total_user_sum}")
        print("======= PLAYER WINS =======")
        break
    ans = int(input(">>> HIT(1) or STAY(2): "))
    if (ans== 1):
        user.append(suit.pop())
        if (calculate(user) > 21):
            display(1)
            total_com_sum = calculate(com)
            total_user_sum = calculate(user)
            print("======= DEALER WINS =======")
            break
        else:
            total_com_sum = calculate(com)
            total_user_sum = calculate(user)

    if ans == 2:
        display(1)
        while total_com_sum <= total_user_sum:
            print("COM HIT...")
            com.append(suit.pop())
            total_com_sum = calculate(com)
            if total_com_sum > 21:
                total_user_sum = calculate(user)
                print(f"COM : {total_com_sum} VS USER : {total_user_sum}")
                print("======= PLAYER WINS =======")
                button = 0
                break

# print(f"COM : {total_com_sum} VS USER : {total_user_sum}")
# if (total_com_sum > total_user_sum):
#     print("======= DEALER WINS =======")
# elif (total_com_sum < total_user_sum):
#     print("======= PLAYER WINS =======")
# else:
#     print("======= DUES ======")

        
        

    

