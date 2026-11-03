# [1] 상속(inheritance)
# 부모 클래스로부터 모든 특성과 행동을 물려받는 행위를 하는 클래스

# 1. Overriding : 부모가 하는 행동을 덮어씌우는 것
# -> 똑같은 이름의 행동(메소드) -> 하는 행동은 달라지는 것

# [2] 다형성 (Polymorphism)
# 2. Overloading : 같은 이름의 메소드의 (1) 전달받는 파라미터의 타입을 바꾼다 (파이썬에는 타입이 없어 존재하지 않음.)
# add(a:int, b:int) a + b
# add(a:string, b:string) 다를 수 있음

# [3] 추상화 (Abstraction)
# 특정 클래스에 대한 skeletion(뼈대)만 만들어두고, 실제 구현은 자식한테 넘기는 것
# -> 추상 클래스 : 추상 클래스는 구현을 할 수 없게 제한

# [4] 캡슐화 (encapsulation)
# 우리들의 정보를 숨기는 것 -> 캡슐화
# 우리가 가진 변수들을 외부에서 직접 접근이 안되도록 하는 것
# -> 직접 접근이 아닌, 무조건 함수(메소드)를 통해서만 접근이 가능하도록 바꾸는 것

class Account():
    def __init__(self):
        #self.balance = 100
        # 1. 변수의 앞에 _ (아무 효과 없음)
        # 1-1 그냥 무지한 사람들이 접근못하게 
        # 1-2. 암묵적인 규칙(내부용 데이터, 건드리지 말기)
        #self._balance = 100
        # 1-3.
        self.__balance = 100

    #getter : 값을 가져오는 함수

    def get_balance(self):
        return self.__balance
        
    #setter : 값을 세팅하는 함수

    def set_balance(self, amount):
        self.__balance += amount

# acc = Account()
# print(acc._balance)

# print(acc._Account__balance)


from abc import ABC, abstractmethod
#ABC : 추상 클래스
#abstractmethod : 이 추상 클래스의 메소드를 호출하지 못하게 막을 방법

# class Animal(ABC):
#     def __init__(self, name):
#         self.name = name
    
#     # -> decorator -> 특정 function(함수)로 이 함수를 감싸준다.
#     # ** 일단 막혀있는 method가 있어야 추상클래스로 인정된다.
#     @abstractmethod
#     def cry(self):
#         print(f"{self.name}이(가) 웁니다.")

# a = Animal('동물')
# print(a.name)

# Dog는 Animal로부터 상속받는 클래스
# class Dog(Animal):

#     def __init__(self, name, breed):
#         #내 부모의 __init__을 일단 호출해서 같은 항목들을 만들어줘
#         super().__init__(name)
#         self.breed = breed

#     def cry(self):
#         super().cry()
#         print("멍멍")

#     def 손(self):
#         print("왈왈(손)")

# dog = Dog("인절미", "웰시코기")
# dog.cry()
# dog.손()
# print(dog.breed)


# 상속 실습
# 1. 추상 클래스 / 부모 클래스인 "도형" 클래스를 만든다.ABC
#       - 특징 : 뭔가
#       - 면적구하기, 둘레 구하기
class Shape():

    def __init__(self, h, w):
        self.h = h
        self.w = w
    
    def get_perimeter(self):
        return ((self.h + self.w)) * 2
    

    def get_area(self):
        return self.h * self.w


# 2. 사각형이라는 클래스를 "도형" 클래스로부터 상속
class Rectangle(Shape):
    def __init__(self, h, w):  
        super().__init__(h, w)

# rec = Rectangle(10 , 20)
# print(rec.get_area())


# 3. 삼각형이라는 클래스를 "도형" 클래스로부터 상속
# -> 둘레 버리기
class Triangle(Shape):
    def __init__(self, h, w):
        super().__init__(h, w)

        def get_area(self):
            return (self.h * self. w) / 2

# tri = Triangle(10, 15)
# print(tri.get_area())

class Account():
    def __init__(self):
        self.__balance = 100

    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, amount):
        self.__balance += amount

# acc = Account()
# print(acc.balance)
# acc.balance = 100000
# print(acc.balance)
