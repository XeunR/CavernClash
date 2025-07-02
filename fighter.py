import random
ID = 0
# ID is used to distinguish identical characters

with open("ally.txt", "r") as allies:
    allies_dict = {}
    for ally in allies:
        ally_list = ally.strip().split("|")
        allies_dict[ally_list[0]] = [ally_list[1], int(ally_list[2]), int(ally_list[3]), int(ally_list[4]),
                                     ally_list[5], int(ally_list[6]), ally_list[7], ally_list[8], ally_list[9]]

with open("enemy.txt", "r") as enemies:
    enemies_dict = {}
    for enemy in enemies:
        enemy_list = enemy.strip().split("|")
        enemies_dict[enemy_list[0]] = [int(enemy_list[1]), int(enemy_list[2]), int(enemy_list[3]),
                                       int(enemy_list[4]), enemy_list[6], int(enemy_list[7])]
    # Removed rarity as it's not needed

with open("gear.txt", "r") as gears:
    weapon_dict = {}
    armour_dict = {}
    for gear in gears:
        gear_list = gear.strip().split("|")
        if gear_list[1] == "Weapon":
            weapon_dict[gear_list[0]] = int(gear_list[3])
        elif gear_list[1] == "Armour":
            armour_dict[gear_list[0]] = int(gear_list[3])

    # Only required information here is the ATK or HP provided by the weapon/armour


class Fighter:
    def __init__(self, name, level):
        global ID
        self.name = name
        self.weapon = None
        self.armour = None
        self.weapon_stone = None
        self.armour_stone = None
        self.positive_effects = {}
        self.negative_effects = {}
        self.id = ID
        ID += 1

        if name in allies_dict:
            stats = allies_dict[name]
            self.role = stats[0]
            if self.role == "DamageSingle" or self.role == "DamageMulti":
                self.base_crit_rate = 0.1
            else:
                self.base_crit_rate = 0.05
            self.base_hp = stats[1] + level
            self.base_atk = stats[2]
            self.base_speed = stats[3]
            self.normal_name = stats[4]
            self.normal_damage = stats[5]
            self.normal_description = stats[6]
            self.skill_name = stats[7]
            self.skill_description = stats[8]

        elif name in enemies_dict:
            stats = enemies_dict[name]
            self.base_hp = stats[1]
            self.base_atk = stats[2]
            self.base_speed = stats[3]
            self.normal_name = stats[4]
            self.normal_damage = stats[5]

        self.hp = self.base_hp
        self.atk = self.base_atk
        self.speed = self.base_speed
        self.crit_rate = 0 # Will be defined later
        try:
            self.next_action = round(10000 / self.speed)
        except ZeroDivisionError:
            self.next_action = -1

    def lose_health(self, health_lost):
        self.hp -= health_lost
        if self.hp <= 0:
            self.hp = 0

    def apply_effects(self):
        self.atk = self.base_atk
        self.speed = self.base_speed
        if self.__class__.__name__ == "Ally":
            self.crit_rate = self.base_crit_rate

        for key_effect, value_effect in self.negative_effects.items():
            if key_effect == "Poisoned":
                self.lose_health(10)
                print(f"{self.name} takes 10 poison damage.")
            elif key_effect == "Burned":
                self.lose_health(20)
                print(f"{self.name} takes 20 burn damage.")
            elif key_effect == "Bleeding":
                self.lose_health(20)
                print(f"{self.name} takes 20 bleed damage.")
            elif key_effect == "Slow":
                self.speed -= round(self.base_speed * 0.1)
            elif key_effect == "Grief":
                self.speed -= round(self.base_speed * 0.05)
                self.atk -= round(self.base_atk * 0.1)
            elif key_effect == "Decay":
                self.atk -= round(self.base_atk * 0.1)
                self.lose_health(20)
                print(f"{self.name} takes 20 decay damage.")
            elif key_effect == "Frozen":
                print(f"{self.name} has lost a turn, but is now unfrozen.")
                try:
                    self.next_action = round(10000 / self.speed)
                except ZeroDivisionError:
                    self.next_action = -1
            self.negative_effects[key_effect] -= 1
            if value_effect == 0:
                del self.negative_effects[key_effect]

        for key_effect, value_effect in self.positive_effects.items():
            self.positive_effects[key_effect] -= 1
            if key_effect == "Alchemist Potion":
                self.crit_rate += 0.15
                self.atk += self.base_atk * 0.15
                self.speed += 0.15
            elif key_effect == "Commanded":
                self.crit_rate += 0.15
                self.atk += self.base_atk * 0.5
            elif key_effect == "Cleric's Faith":
                self.atk += self.base_atk * 0.6
                self.speed += 0.1
            self.negative_effects[key_effect] -= 1
            if value_effect == 0:
                del self.positive_effects[key_effect]


class Ally(Fighter):
    def __init__(self, name, level):
        super().__init__(name, level)
        self.crit_rate = None

    def calculate_equipment(self, level):
        stats = allies_dict[self.name]
        self.role = stats[0]
        if self.role == "DamageSingle" or self.role == "DamageMulti":
            self.base_crit_rate = 0.1
        else:
            self.base_crit_rate = 0.05
        self.base_hp = stats[1] + level
        self.base_atk = stats[2]
        self.base_speed = stats[3]
        self.normal_name = stats[4]
        self.normal_damage = stats[5]
        self.normal_description = stats[6]
        self.skill_name = stats[7]
        self.skill_description = stats[8]

        if self.weapon:
            self.base_atk += weapon_dict.get(self.weapon)

        if self.weapon_stone:
            amplifier = self.weapon_stone[0][1]
            buff = self.weapon_stone[1]
            if buff == "Critical":
                self.base_crit_rate *= 1 + (0.05 * amplifier)
            elif buff == "Damage":
                self.base_atk *= 1 + (0.05 * amplifier)
            elif buff == "Health":
                self.base_hp *= 1 + (0.05 * amplifier)
            elif buff == "Swiftness":
                self.base_speed *= 1 + (0.05 * amplifier)

        if self.armour:
            self.base_hp += armour_dict.get(self.armour)

        if self.armour_stone:
            amplifier = self.armour_stone[0][1]
            buff = self.armour_stone[1]
            if buff == "Critical":
                self.base_crit_rate *= 1 + (0.05 * amplifier)
            elif buff == "Damage":
                self.base_atk *= 1 + (0.05 * amplifier)
            elif buff == "Health":
                self.base_hp *= 1 + (0.05 * amplifier)
            elif buff == "Swiftness":
                self.base_speed *= 1 + (0.05 * amplifier)

        self.hp = self.base_hp
        self.atk = self.base_atk
        self.speed = self.base_speed
        self.crit_rate = self.base_crit_rate

    def normal(self):
        normal_damage = round(self.atk * self.normal_damage / 100) + random.randint(-5, 5)
        critical = random.random()
        crit_display = False
        if critical <= self.crit_rate:
            normal_damage = round(normal_damage * 1.5)
            crit_display = True
        return normal_damage, crit_display

    # Unique skills of each character
    def skill_motivated_charge(self):
        skill_damage = round(self.atk * 2) + random.randint(-5, 5)
        critical = random.random()
        crit_display = False
        if critical <= self.crit_rate:
            skill_damage = round(skill_damage * 1.5)
            crit_display = True
        return skill_damage, crit_display

    def skill_with_all_our_might(self):
        skill_damage = round(self.atk * 2) + random.randint(-5, 5)
        critical = random.random()
        crit_display = False
        if critical <= self.crit_rate + 0.2:
            skill_damage = round(skill_damage * 1.5)
            crit_display = True
        return skill_damage, crit_display

    def skill_meteor_shower(self):
        skill_damage = round(self.atk * 1.2) + random.randint(-5, 5)
        critical = random.random()
        crit_display = False
        if critical <= self.crit_rate:
            skill_damage = round(skill_damage * 1.5)
            crit_display = True
        return skill_damage, crit_display

    def skill_icicle_shower(self):
        skill_damage = round(self.atk * 0.5) + random.randint(-5, 5)
        critical = random.random()
        crit_display = False
        if critical <= self.crit_rate:
            skill_damage = round(skill_damage * 1.5)
            crit_display = True
        return skill_damage, crit_display

    def skill_sneak(self):
        skill_damage = round(self.atk * 1.5) + random.randint(-5, 5)
        critical = random.random()
        crit_display = False
        if critical <= self.crit_rate:
            skill_damage = round(skill_damage * 1.5)
            crit_display = True
        return skill_damage, crit_display

    def skill_in_honour_of_harry(self):
        skill_damage = round(self.atk * 10) + random.randint(-5, 5)
        critical = random.random()
        crit_display = False
        if critical <= self.crit_rate:
            skill_damage = round(skill_damage * 1.5)
            crit_display = True
        return skill_damage, crit_display

    def skill_big_booms(self):
        skill_damage = round(self.atk * 1.75) + random.randint(-5, 5)
        critical = random.random()
        crit_display = False
        if critical <= self.crit_rate:
            skill_damage = round(skill_damage * 1.5)
            crit_display = True
        return skill_damage, crit_display

    def skill_dark_magic_spell(self):
        skill_damage = round(self.atk * 0.7) + random.randint(-5, 5)
        critical = random.random()
        crit_display = False
        if critical <= self.crit_rate:
            skill_damage = round(skill_damage * 1.5)
            crit_display = True
        return skill_damage, crit_display


class Enemy(Fighter):
    def __init__(self, name, level):
        super().__init__(name, level)

    def normal(self):
        normal_damage = round(self.atk * self.normal_damage / 100) + random.randint(-5, 5)
        return normal_damage

    # Custom AI
    def special(self):
        pass
