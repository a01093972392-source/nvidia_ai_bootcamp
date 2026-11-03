#파일 입출력
#1.파일 쓰기
#2.파일 읽기
#3.파일에 추가하기

# open(파일명, mode)
# modes
# 'w' : 쓰기 모드 -> 없으면 새로 만들어짐

# 있다면 -> 덮어씌운다.
# f = open("test.txt", 'w', encoding = 'utf8')
# # 파일에 쓸때에는 무조건 문자열만 들어간다.
# f.write(str(123) + '\n')
# f.write(f"{456}\n")
# f.write("안녕하세요\n")
# f.write("저는 홍길동입니다.\n")
# # 파일을 안전하게 닫는다는 의미
# f.close()

# # -- 파일 작업을 할 때 많이 쓰는 문법
# # with open
# # 1. name aliasing -> 이 파일 이름을 f로 씀
# # 2. 코드가 종료되면 -> close()도 알아서 동작.
# with open("file.txt", 'w') as f:
#     f.write("1234")

###########################################
# 파일 읽기
# mode : 'r' (read)
# with open('file.txt', 'r', encoding = 'utf8') as f:
    # 1. read
    # a = f.read() # 파일 전체를 읽어온다.
    # print(a)




    # 2. readline
    # print(f.readline()) #호출할 때마다 한줄씩 읽어온다
    # print(f.readline())
    # print(f.readline())


    # 3. readlines
    # print(f.readlines()) #줄마다 끊어서 리스트로 변환해서 가져옴


###############################################
# 파일에 추가하기
# with open('file.txt', 'a', encoding = 'utf8') as f:
#     f.write('\n새롭게 추가한 줄입니다.\n')



# 실습1: 영단어 테스트 프로그램
import random as rd
d = {} 

with open('words.txt', 'r', encoding = 'utf8') as f:
    li = f.readlines()
    for i in li:
        k,v = i[:-1].split(":")
        d[k] = v

print("##1.영단어 테스트 하기##")
print("##2.영단어 추가하기##")
n = int(input("영단어 테스트 하기(1) or 영단어 추가하기(2): "))
if (n == 1):
    # d = {} 

    # with open('words.txt', 'r', encoding = 'utf8') as f:
    #     li = f.readlines()
    #     for i in li:
    #         k,v = i[:-1].split(":")
    #         d[k] = v

    keys = list(d.keys())
    rd.shuffle(keys)
    
    print("=== 영단어 테스트의 시작 ===")
    print("제시되는 영단어의 한글 뜻을 입력하세요.")

    ans_count = 0
    total_ques = 0
    for k in keys:
        print(f"단어 [{k}]의 뜻: ", end = ' ')
        ans = input()
        if (ans == d[k]):
            print("-> 정답입니다!")
            total_ques += 1
            ans_count += 1
        else:
            print(f"오답! 정답은 {d[k]} 입니다")
            total_ques += 1
            continue
    

    percent = int((ans_count / total_ques) * 100)
    print("=== 테스트 종료 ===")
    print(f"최종 점수: {ans_count} / {total_ques} (정답률: {percent}%)")

if (n == 2):
    print("=== 영단어 추가하기 ===")
    print("영단어:뜻 형태로 입력하시오")
    print("추가가 완료되면 end를 입력하시오")

    while True:
        new_word = input().replace(" ", "")
        
        # 'end' 입력 시 파일에 작성하지 않고 즉시 반복문 탈출
        if new_word == "end":
            print("단어 추가가 완료되었습니다.")
            break

        new_word_key = new_word.split(':')[0]
        if new_word_key in d.keys():
            print("이미 존재하는 단어입니다. 다른 단어를 추가해주세요!")
            continue

        with open('words.txt', 'a', encoding='utf8') as f:
            f.write(f"{new_word}\n")


#실습 2