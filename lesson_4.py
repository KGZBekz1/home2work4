import random


# Базовый класс персонажа
class Hero:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack
        self.alive = True

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def is_alive(self):
        return self.alive


# Класс босса
class Boss:
    def __init__(self, health, attack):
        self.health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0


# Witcher: жертвует собой для возрождения другого героя
class Witcher(Hero):
    def __init__(self, name, health, attack):
        super().__init__(name, health, attack)
        self.revive_used = False

    def revive(self, team):
        if not self.revive_used:
            for hero in team:
                if not hero.is_alive():
                    print(f"{self.name} жертвует собой, чтобы возродить {hero.name}")
                    hero.health = hero.health // 2  # Возвращает часть здоровья
                    hero.alive = True
                    self.alive = False
                    self.revive_used = True
                    break


# Magic: увеличивает атаку всей команды после каждого раунда
class Magic(Hero):
    def __init__(self, name, health, attack, boost):
        super().__init__(name, health, attack)
        self.boost = boost

    def increase_attack(self, team):
        for hero in team:
            if hero.is_alive():
                hero.attack += self.boost
                print(f"Атака {hero.name} увеличена на {self.boost}")


# Hacker: крадет здоровье босса и передает одному из героев
class Hacker(Hero):
    def __init__(self, name, health, attack, steal_amount):
        super().__init__(name, health, attack)
        self.steal_amount = steal_amount

    def steal_health(self, boss, team):
        if boss.health > self.steal_amount:
            boss.take_damage(self.steal_amount)
            hero = random.choice([h for h in team if h.is_alive()])
            hero.health += self.steal_amount
            print(f"{self.name} украл {self.steal_amount} здоровья у босса и передал его {hero.name}")


# Дополнительные герои
# Golem: принимает 1/5 урона от босса для других героев
class Golem(Hero):
    def __init__(self, name, health, attack):
        super().__init__(name, health, attack)

    def absorb_damage(self, damage):
        absorbed = damage // 5
        self.take_damage(absorbed)
        print(f"{self.name} принял на себя {absorbed} урона")


# Thor: имеет шанс оглушить босса на 1 раунд
class Thor(Hero):
    def __init__(self, name, health, attack, stun_chance):
        super().__init__(name, health, attack)
        self.stun_chance = stun_chance

    def try_stun(self, boss):
        if random.random() < self.stun_chance:
            print(f"{self.name} оглушил босса!")
            return True
        return False


# Пример реализации раунда
def round_fight(heroes, boss):
    for hero in heroes:
        if hero.is_alive():
            # Герои атакуют босса
            boss.take_damage(hero.attack)
            print(f"{hero.name} наносит {hero.attack} урона боссу")

    if boss.is_alive():
        print(f"Босс атакует команду!")
        # Босс атакует всех героев
        for hero in heroes:
            if hero.is_alive():
                damage = boss.attack
                if isinstance(hero, Golem):
                    hero.absorb_damage(damage)
                else:
                    hero.take_damage(damage)
                print(f"{hero.name} получает {damage} урона")


# Инициализация героев и босса
witcher = Witcher("Witcher", 100, 20)
magic = Magic("Magic", 80, 15, 5)
hacker = Hacker("Hacker", 70, 10, 15)
golem = Golem("Golem", 150, 10)
thor = Thor("Thor", 90, 25, 0.3)

heroes = [witcher, magic, hacker, golem, thor]
boss = Boss(500, 30)
# Пример игры

round_num = 1
while boss.is_alive() and any(hero.is_alive() for hero in heroes):
    print(f"\n--- Раунд {round_num} ---")
    round_fight(heroes, boss)

    # Способности героев
    magic.increase_attack(heroes)
    hacker.steal_health(boss, heroes)

    # Оживление героев Ведьмаком
    if not witcher.is_alive() and not witcher.revive_used:
        witcher.revive(heroes)

    round_num += 1

if boss.is_alive():
    print("Босс победил!")
else:
    print("Герои победили!")
