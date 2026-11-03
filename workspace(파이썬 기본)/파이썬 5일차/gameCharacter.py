#gameCharacter.py

import random

class Character():
    
    def __init__(self, hp, max_hp, name, dice_num):
        self.hp = hp
        self.max_hp = max_hp
        self.name = name
        self.dice_num = dice_num
    
    def roll(self):
        rolls = []
        for i in range(self.dice_num):
            rolls.append(random.randint(1, 6))
        print(f"<<{self.name}의 주사위 : {rolls}>>")
        return rolls

    def attack(self, other):
        li = self.roll()
        attack_damage = sum(li)
        other.hp -= attack_damage
        print(f"{self.name}가 {other.name}에게 {attack_damage} 데미지를 주었다! ({other.name} 남은 체력: {other.hp})")
        return attack_damage
        
    def heal(self):
        print(f"---{self.name}가 회복을 시도한다!---")
        li = self.roll()
        heal_hp = sum(li)
        self.hp += heal_hp
        
        if self.hp > self.max_hp:
            self.hp = self.max_hp
            print(f"{self.name}의 체력이 최대치({self.max_hp})가 되었다!")
        else:
            print(f"{self.name}가 {heal_hp} 만큼 회복했다! (현재 체력: {self.hp})")
            
        return heal_hp
    
    def info(self):
        print(f"==== [{self.name}] 기본 정보 ====")
        print(f"체력: {self.hp} / {self.max_hp}")
        print(f"굴리는 주사위 개수: {self.dice_num}개")


class Warrior(Character):

    def __init__(self, name="전사"):
        super().__init__(100, 100, name, 2)
    
    def attack(self, other):
        li = self.roll() 
        if li[0] == li[1]:
            damage = ((li[0] + li[1]) * 2)
            other.hp -= damage
            print(f"[크리티컬!] {self.name}가 {other.name}에게 {damage} 만큼 피해를 주었다! ({other.name} 남은 체력: {other.hp})")
        else:
            damage = sum(li)
            other.hp -= damage
            print(f"{self.name}가 {other.name}에게 {damage} 데미지를 주었다! ({other.name} 남은 체력: {other.hp})")
            
    def heal(self):
        li = self.roll()
        if li[0] == li[1]:
            print(f"---{self.name}가 대회복을 시도한다!---")
            heal_hp = ((li[0] + li[1]) * 2)
            self.hp += heal_hp
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            print(f"[대성공!] {self.name}가 {heal_hp} 만큼 회복했다! (현재 체력: {self.hp})")
        else:
            print(f"---{self.name}가 회복을 시도한다!---")
            heal_hp = sum(li)
            self.hp += heal_hp
            if self.hp > self.max_hp:
                self.hp = self.max_hp
                print(f"{self.name}의 체력이 최대치({self.max_hp})가 되었다!")
            else:
                print(f"{self.name}가 {heal_hp} 만큼 회복했다! (현재 체력: {self.hp})")
                
    def info(self):
        super().info()
        print("[전투 특성]")
        print("- 기본 공격: 두 주사위 눈의 합만큼 데미지를 줍니다.")
        print("- 크리티컬: 두 주사위의 눈이 같으면 합의 2배만큼 피해를 주고, 회복 시에도 2배로 회복합니다.\n")


class Rogue(Character): 
    
    def __init__(self, name="도적"):
        super().__init__(75, 75, name, 2)

    def attack(self, other):
        li = self.roll()
        
        if (li[0] % 2 == li[1] % 2): 
            extra_rolls = self.roll()
            li.extend(extra_rolls)
            
            damage = sum(li)
            other.hp -= damage
            print(f"[연속 공격!] {self.name}가 {other.name}에게 {damage} 만큼 피해를 주었다! ({other.name} 남은 체력: {other.hp})")
            return damage
        else:
            damage = sum(li)
            other.hp -= damage
            print(f"{self.name}가 {other.name}에게 {damage} 데미지를 주었다! ({other.name} 남은 체력: {other.hp})")
            return damage
            
    def heal(self):
        li = self.roll()
        heal_hp = 0
        if (li[0] % 2 == li[1] % 2):
            heal_hp = 20
            self.hp += heal_hp
            if self.hp > self.max_hp:
                self.hp = self.max_hp
                print(f"{self.name}의 체력이 최대치({self.max_hp})가 되었다!")
            else:
                print(f"{self.name}가 {heal_hp} 만큼 회복했다! (현재 체력: {self.hp})")
        else:
            heal_hp = sum(li)
            self.hp += heal_hp
            if self.hp > self.max_hp:
                self.hp = self.max_hp
                print(f"{self.name}의 체력이 최대치({self.max_hp})가 되었다!")
            else:
                print(f"{self.name}가 {heal_hp} 만큼 회복했다! (현재 체력: {self.hp})")
                
    def info(self):
        super().info()
        print("[전투 특성]")
        print("- 기본 공격: 두 주사위 눈의 합만큼 데미지를 줍니다.")
        print("- 연속 공격: 두 주사위가 모두 짝수이거나 홀수이면, 주사위를 한 번 더 굴려 합산 데미지를 줍니다.\n")


class Magician(Character):

    def __init__(self, name="마법사"):
        super().__init__(50, 50, name, 3)
    
    def attack(self, other):
        li = self.roll()
        if sum(li) == 18:
            damage = 100
            other.hp -= damage
            print(f"[메테오 스트라이크!] {self.name}가 {other.name}에게 {damage}의 치명적인 피해를 주었다! ({other.name} 남은 체력: {other.hp})")
        elif sum(li) == 3:
            self.hp = 0
            print(f"[마법 폭주!] {self.name}의 마법이 역류하여 스스로 목숨을 잃었습니다... (현재 체력: {self.hp})")
        elif li[0] % 2 == li[1] % 2 == li[2] % 2:
            damage = sum(li) * 2
            other.hp -= damage
            print(f"[더블 캐스팅!] {self.name}가 {other.name}에게 {damage} 만큼 피해를 주었다! ({other.name} 남은 체력: {other.hp})")
        elif sorted(li)[0] + 1 == sorted(li)[1] and sorted(li)[1] + 1 == sorted(li)[2]:
            damage = 45
            other.hp -= damage
            print(f"[연쇄 번개!] {self.name}가 {other.name}에게 {damage} 만큼 피해를 주었다! ({other.name} 남은 체력: {other.hp})")
        else:
            damage = max(li)
            other.hp -= damage
            print(f"{self.name}가 {other.name}에게 {damage} 데미지를 주었다! ({other.name} 남은 체력: {other.hp})")
    
    def heal(self):
        li = self.roll()
        heal_hp = 0
        if li[0] == li[1] == li[2]:
            self.hp = self.max_hp
            print(f"{self.name}의 체력이 최대치({self.max_hp})가 되었다!")
        elif li[0] % 2 == li[1] % 2 == li[2] % 2:
            heal_hp = 30
            self.hp += heal_hp
            if self.hp > self.max_hp:
                self.hp = self.max_hp
                print(f"{self.name}의 체력이 최대치({self.max_hp})가 되었다!")
            else:
                print(f"{self.name}가 {heal_hp} 만큼 회복했다! (현재 체력: {self.hp})")
        else:
            heal_hp = sum(li)
            self.hp += heal_hp
            if self.hp > self.max_hp:
                self.hp = self.max_hp
                print(f"{self.name}의 체력이 최대치({self.max_hp})가 되었다!")
            else:
                print(f"{self.name}가 {heal_hp} 만큼 회복했다! (현재 체력: {self.hp})")
                
    def info(self):
        super().info()
        print("[전투 특성]")
        print("- 메테오(합 18): 100의 고정 데미지를 줍니다.")
        print("- 더블 캐스팅(모두 짝수/홀수): 합의 2배 데미지를 줍니다.")
        print("- 연쇄 번개(주사위 눈이 연속된 숫자): 45의 고정 데미지를 줍니다.")
        print("- 일반 공격: 주사위 눈 중 가장 큰 숫자만큼만 데미지를 줍니다.")
        print("- 마법 폭주(합 3): 즉사합니다.\n")