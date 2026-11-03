#tuple - iterable, sequence, immutable
#튜플: 기본적으로 리스트와 동일
#다른점이 하나 -> immutable(불변)
#리스트와 똑같은데 요소가 변경되지 않음.
#[] {} ()
tu = tuple() #비어있는 튜플
#사용처: 1. 데이터를 외부에서 접근해서 바꾸면 안되는 경우
#       2. list 안에 list를 계속 append하면서 중첩리스트를 만들수 있음
#          list를 append하는것보다는 tuple을 append하는게 속도가 더 빠름


#set - iterable, mutable
#고유의 값들만 보유한 데이터
# s = {1, 2, 3, 4, 1, 2, 5, 6}
# # li = {1, 1, 0, 3, 2, 1, 2, 3, 5}
# # s = set(li)
# # print(s)
# a = {1, 2, 3, 4, 5}
# b = {3, 4, 5, 6, 7}
# #intersect (두 그룹에 같이 존재하는 요소만 filter)
# print(a & b) #and

# #union (한 그룹에라도 존재하는것을 합치는 것 -> 두 그룹의 고유값들을 합친다.)
# print(a | b) #or

# #difference(한 그룹에서 다른 그룹에 존재하는것을 뺀 새로운 그룹(겹치는거 뺀것))
# print(a -b)

# #symmetric difference(양쪽에 겹치지 않는 것들만 추출)
# print(a ^ b)




#dictionary - iterable, mutable, hashtable
#사전: a(key) 라는걸 찾으면 그거에 매핑된 b(value)값을 찾아옴
#1. key와 value pair로 이루어진 자료 구조
#리스트와 거의 똑같이 쓰는데, index가 순번이 아니라 -> 우리가 저장할려고 하는 단어든 숫자던 그런걸로 저장

d = {
    "apple": "사과",
    "watermelon": "수박",
    1 : "one",
    "class": [1, 2, 3, 4],
    (1, 1): 'tuple'
}

print(d["apple"])  #d[key] -> 이 key에 mapping된 value를 찾아옴.
# print(d['사과']) #만약 내가 없는 key에 접근하려고 한다면 -> error


#딕셔너리에 대해서 단순한 for문을 돌리면 key값만 나옴.
for i in d:
    print(i)


#딕셔너리의 데이터를 분해해서 접근할 수 있는 방법 3개
#1.d.keys()
for k in d.keys():
    print(k, end = ' ')
print()
#2 d.values()
for v in d.values():
    print(v, end = ' ')
print()
#3 d.items()
print(d.items())

for i in d.items():
    print(f"key: {i[0]}, value: {i[1]}")

for k , v in d.items():
    print(f"key: {k}, value: {v}")


############################################
#모든 자료구조에 대해 써야 하는것 3개
#1.접근
print(d.get('사과'))   #key가 존재하지 않으면, None이라는게 나온다.and

#2.삽입
d['banana'] = '바나나'
print(d)
#만약 이미 존재하는 keyt를 넣으면
#기존에 존재하는 key를 넣으면 -> 이전의 key, value pair가 update됨.abs
#2. 고유의 key만을 관리하는 자료구조

#3 삭제
del d['apple']
print(d)

d.pop('banana') #이렇게 사용하는 것을 권장!

################################################
#딕셔너리를 사용하는 용도
#list vs dictionary
#문자열이나 엄청 큰 숫자나 그런것에 대한 어떤한 연결된 값을 저장하기 위해 사용한다


#가장 많이 쓰는 형태
#보통 counting을 위해 많이 쓴다

li = [1, 3, 5, 7, 9, 1, 2, 3 ,4, 5, 3, 4, 5, 6, 7]

#1. 순정

d = {}
for i in li:
    #d[i]에 접근했을 때 이미 존재하느냐 하지 않느냐의 검증이 필요
    if d.get(i) != None: #i라는 숫자를 발견한 적이 있음.   or if i in d.keys()
        d[i] += 1
    else: #i라는 숫자의 키가 존재하지 않다면
        d[i] = 1
print(d)

#2. defaultdict -> 만약 존재하지 않는 key에 update를 할려고할 때, 알아서 기본값을 세팅해주는 애

from collections import defaultdict
d = defaultdict(int) #value는 default로 int값을 가지고, 0으로 시작
for i in li:
    d[i] += 1
print(d)

#3. python 라이브러리 함수 이용
from collections import Counter
d = Counter(li)
print(d)

d = {3:3, 4:4}
e = {1:1, 2:2}
d.update(e)
print(d)