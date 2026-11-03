#class
#파이썬은 모든 것이 객체이다 -> object
#객체지향 프로그래밍 -> object oriented programming -> OOP
#모든 것이 객체로 이루어진 환경이다.

#OOP -> 실제 세상을 반영해서 만드는 프로그래밍 방법

# blueprint - 청사진(몰드)
# -> instance

# class Dog(): # 문법 규칙: class는 만들 때 명사형으로, 첫 단어는 대문자
    #1. 속성 (attribute) => 변수
    #생성자(constructor): 이 class를 가지고 instance를 만들 때 처음으로 호출되는 함수
    
    # def __init__(self, breed, age):
    #     self.breed = breed
    #     self.age = age
    #     self.li = []

    #2. 메소드 (method) => 함수
    # def eat(self,food):
    #     print(f"{self.breed}(이)가 {food}(을)를 맛있게 먹는다.")
    
    #모든 메소드의 첫번 째 매개변수는 항상 자기 자신을 가리켜야 한다.
    # def bark(self):
    #     print("멍멍")

# dog1 = Dog('콜라', 3) # dog = Dog()라는 몰드로 찍어낸 'object' -> 인스턴스
# print(dog1.breed, dog1.age)
# dog1.bark()
# dog1.eat("뼈다귀")

# dog2 = Dog('사이다', 4)
# dog2.breed = '흰둥이'
# dog2.age = 15
# print(dog2.breed, dog2.age)

# print(dog1.li, dog2.li)
# dog1.li.append(10)
# print(dog1.li, dog2.li)

#################################################
# class 클래스명():
#     #생성자
#     def __init__(self):
#         #속성들
#         #생성되는 시점부터 바뀌거나 고유해야하는 값들은 여기서 매개변수로 전달

#     def 메소드(self):
#         # 이 클래스가 할 수 있는 행동



####################################################
# 실습1. 계산기 자체를 만들기

# class Calculator():
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
    
#     def add(self):
#         print(f"{self.a} + {self.b} = ", self.a + self.b)

#     def minus(self):
#         print(f"{self.a} - {self.b} = ", self.a - self.b)
    
#     def multiply(self):
#         print(f"{self.a}  X  {self.b} = ", self.a * self.b)
    
#     def divide(self):
#         try:
#             print(f"{self.a} / {self.b} = ", self.a / self.b)

#         except ZeroDivisionError:
#             return Error

# cal = Calculator(3, 5).divide()

# 실습2. 사각형
# -> attribute: height, width
# -> method: 둘레 구하기, 면적 구하기

# class Rectangle():
#     def __init__(self, h, w):
#         self.h = h
#         self.w = w

#     def rec_perimeter(self):
#         perimeter = 2 * (self.h + self.w)
#         print(f"높이가 {self.h}이고 너비가 {self.w}인 사각형의 둘레는: {perimeter}입니다")
    
#     def rec_area(self):
#         area = self.h * self.w
#         print(f"높이가 {self.h}이고 너비가 {self.w}인 사각형의 넓이는: {area}입니다")

# rec1 = Rectangle(10, 20)
# rec2 = Rectangle(4, 10)
# rec1.rec_area(), rec2.rec_area()

#실습3. 원
#-> attribute : 반지름
#-> method: 둘레 구하기, 면적 구하기

# class Circle():
#     def __init__(self, r):
#         self.r = r
    
#     def cir_round(self):
#         round = 2 * 3.14 * self.r
#         print(f"반지름의 길이가 {self.r}인 원의 둘레는 : {round} 입니다")

#     def circle_area(self):
#         area = 2 * 3.14 * (self.r ** 2)
#         print(f"반지름의 길이가 {self.r}인 원의 넓이는 : {area} 입니다")

#cir = Circle(10).circle_area()



#실습 1
# import random

# class BankAccount():

#     def __init__(self, name, username, password):
#         self.name = name
#         self.balance = 0
#         self.number = random.randint(10000000, 99999999)
#         self.username = username
#         self.password = password
    
#     def info(self):
#         print(f"이름 : {self.name}")
#         print(f"계좌번호 : {self.number}")
#         print(f"잔액 : {self.balance}")
    
#     def deposit(self, n):
#         print(f"{n}원을 입급하셨습니다.")
#         self.balance += n
#         print(f"잔액: {self.balance}")

#     def withdraw(self, n):
#         if (self.balance < n):
#             print("잔액이 부족합니다.")
#             print(f"잔액 : {self.balance}")
        
#         else:
#             print(f"{n}원을 출금했습니다.")
#             self.balance -= n
#             print(f"잔액 : {self.balance}")


# a = BankAccount("최성규", "csg", 1234)
# account.deposit(10000000)
# account.withdraw(10000)
# account.info()


# print(accounts)

#실습 2
# class BankApp():
#     def __init__(self):
#         self.accounts = {}

#     def register(self):
#         print("========")
#         print("신규 가입")
#         print("========")
#         name = input(" >> 이름 : ")
#         username = input(" >> username : ")
#         password = int(input(" >> password : "))
#         self.accounts[username] = BankAccount(name, username, password)
#         print("계좌 생성 성공")
    
#     def login(self):
        
#         while True:
#             print("========")
#             print("로그인")
#             print("========")
#             username = input(" >> username : ")
#             password = int(input(" >> password : "))
#             if (username in self.accounts) and (self.accounts[username].password == password):
#                 print("로그인 성공") 
            
#                 current_user = self.accounts[username]
#                 current_user.info()
#                 while True:
#                     print("========")
#                     print("Options")
#                     print("========")
#                     o = int(input(" >> 1 : 입금 2 : 출금  3 : 로그아웃"))
#                     if (o == 1):
#                         amount = int(input(" >> 입금할 금액을 입력하세요: "))
#                         current_user.deposit(amount)
#                     elif (o == 2):
#                         amount = int(input(" >> 출금할 금액을 입력하세요: "))
#                         current_user.withdraw(amount)
#                     elif (o == 3):
#                         print("로그아웃 합니다.")
#                         return 
#             else:
#                 print("아이디 또는 비밀번호를 확인하세요")
                

#     def run(self):
#         while True:
#             print("========")
#             print("BankApp")
#             print("========")
#             n = int(input(" >> 1: 계좌 생성 2 : 로그인 3 : 종료 "))
#             if (n == 1):
#                 self.register()
        
#             elif (n == 2):
#                 self.login()
        
#             elif (n == 3):
#                 print("종료합니다.")
#                 break

        
# app = BankApp()
# app.run()









# 실습 3(database 저장)

import random

class BankAccount():

    def __init__(self, name, username, password):
        self.name = name
        self.balance = 0
        self.number = random.randint(10000000, 99999999)
        self.username = username
        self.password = password
    
    def info(self):
        print(f"이름 : {self.name}")
        print(f"계좌번호 : {self.number}")
        print(f"잔액 : {self.balance}")
    
    def deposit(self, n):
        print(f"{n}원을 입급하셨습니다.")
        self.balance += n
        print(f"잔액: {self.balance}")

    def withdraw(self, n):
        if (self.balance < n):
            print("잔액이 부족합니다.")
            print(f"잔액 : {self.balance}")
        
        else:
            print(f"{n}원을 출금했습니다.")
            self.balance -= n
            print(f"잔액 : {self.balance}")


class BankApp():
    def __init__(self):
        self.accounts = {}
        self.import_file()

    def import_file(self):
        try:
            with open("database.txt", 'r', encoding = 'utf8') as f:
                li = f.readlines()
                for i in li:
                    username, password, name, number, balance = i.strip().split(',')

                    account = BankAccount(name, username, int(password))
                    account.number = int(number)
                    account.balance = int(balance)
                    self.accounts[username] = account

        except FileNotFoundError:
            pass

    def update_file(self):
        with open("database.txt", 'w', encoding='utf8') as f:
            for user in self.accounts.values():
                f.write(f"{user.username},{user.password}, {user.name}, {user.number},{user.balance}\n")
    
    def register(self):
        print("========")
        print("신규 가입")
        print("========")
        name = input(" >> 이름 : ")
        username = input(" >> username : ")
        password = int(input(" >> password : "))
        self.accounts[username] = BankAccount(name, username, password)
        
        self.update_file()
        print("계좌 생성 성공")
    
    def login(self):
        
        while True:
            print("========")
            print("로그인")
            print("========")
            username = input(" >> username : ")
            password = int(input(" >> password : "))
            if (username in self.accounts) and (self.accounts[username].password == password):
                print("로그인 성공") 
            
                current_user = self.accounts[username]
                current_user.info()
                while True:
                    print("========")
                    print("Options")
                    print("========")
                    o = int(input(" >> 1 : 입금 2 : 출금  3 : 로그아웃"))
                    if (o == 1):
                        amount = int(input(" >> 입금할 금액을 입력하세요: "))
                        current_user.deposit(amount)
                    elif (o == 2):
                        amount = int(input(" >> 출금할 금액을 입력하세요: "))
                        current_user.withdraw(amount)
                    elif (o == 3):
                        print("로그아웃 합니다.")
                        return 
            else:
                print("아이디 또는 비밀번호를 확인하세요")
                

    def run(self):
        while True:
            print("========")
            print("BankApp")
            print("========")
            n = int(input(" >> 1: 계좌 생성 2 : 로그인 3 : 종료 "))
            if (n == 1):
                self.register()

            elif (n == 2):
                self.login()
        
            elif (n == 3):
                print("종료합니다.")
                break


app = BankApp()
app.run()