#dice_battle.py

import random
import time
import os
from gameCharacter import Character, Warrior, Rogue, Magician

class Game():

    def player_action(self):
        ctrl = int(input(f"\n{self.player.name}의 차례: 공격(1)  회복(2) :  "))
        if ctrl == 1:
            self.player.attack(self.enemy)
        elif ctrl == 2:
            self.player.heal()

    def enemy_action(self):
        print(f"\n--- {self.enemy.name}의 턴 ---")
        ctrl = random.randint(1, 2)
        if ctrl == 1:
            self.enemy.attack(self.player)
        elif ctrl == 2:
            self.enemy.heal()

    def display(self):
        print(f"\n======== 라운드 {self.round} ========")
        print(f"[Player] {self.player.name}", f"[Enemy] {self.enemy.name}", sep='\t\t')
        print(f"HP: {self.player.hp} / {self.player.max_hp}", f"HP: {self.enemy.hp} / {self.enemy.max_hp}", sep='\t\t')
        print("============================")
    
    def load(self):
        time.sleep(2)
        # 운영체제에 상관없이 화면이 깨끗하게 지워지도록 수정
        os.system("cls" if os.name == "nt" else "clear")

    def run(self):
        # 1. 캐릭터 선택 루프 (설명을 보더라도 게임이 터지지 않도록 while문으로 보호)
        while True:
            c = int(input("캐릭터를 선택하세요 : 전사(1), 도적(2), 마법사(3), 캐릭터 설명(4) : "))
            if c == 1:
                self.player = Warrior()
                break
            elif c == 2:
                self.player = Rogue()
                break
            elif c == 3:
                self.player = Magician()
                break
            elif c == 4:
                print("\n")
                Warrior().info()
                Rogue().info()
                Magician().info()
                print("===============================\n")

        self.round = 1
        
        # 2. 전투 루프
        while True:
            # 적 스폰 로직 수정 (c가 아닌 ctrl 변수를 사용하여 랜덤하게 적 생성)
            ctrl = random.randint(1, 3)
            if ctrl == 1:
                self.enemy = Warrior("적 전사")
            elif ctrl == 2:
                self.enemy = Rogue("적 도적")
            elif ctrl == 3:
                self.enemy = Magician("적 마법사")

            print(f"\n야생의 {self.enemy.name}이(가) 나타났다!")
            self.load()

            # 현재 라운드의 교전 루프
            while self.player.hp > 0 and self.enemy.hp > 0:
                self.display()
                self.player_action()
                
                if self.enemy.hp <= 0:
                    break
                self.load()
                
                self.display()
                self.enemy_action()
                
                if self.player.hp <= 0:
                    break
                self.load()

            # 승패 판정
            if self.player.hp > 0:
                print(f"\n{self.player.name}이(가) 이겼습니다!")
                self.round += 1
                
                # 승리 시 회복량 계산
                heal_amount = self.player.max_hp // 2
                self.player.hp = min(self.player.hp + heal_amount, self.player.max_hp)
                print(f"승리 보상으로 체력을 회복했습니다. (현재 체력: {self.player.hp} / {self.player.max_hp})")
                self.load()
            else:
                print(f"\n{self.enemy.name}에게 패배했습니다... 게임 오버.")
                break

# 실행 코드
if __name__ == "__main__":
    app = Game()
    app.run()
