import random, time, fighter

def print_potential_targets(team_list):
    if len(team_list) == 1:
        print(f"(1) {team_list[0].name}")
    elif len(team_list) == 2:
        print(f"(1) {team_list[0].name} | (2) {team_list[1].name}")
    elif len(team_list) == 3:
        print(f"(1) {team_list[0].name} | (2) {team_list[1].name} | (3) {team_list[2].name}")


class BattleManager:
    def __init__(self, characters, level):
        # Characters (string): Fighter objects
        self.p1 = characters[0]
        self.p2 = characters[1]
        self.p3 = characters[2]
        self.e1 = characters[3]
        self.e2 = characters[4]
        self.e3 = characters[5]
        self.player_team = [self.p1, self.p2, self.p3]
        self.enemy_team = [self.e1, self.e2, self.e3]
        self.characters = [self.p1, self.p2, self.p3, self.e1, self.e2, self.e3]
        self.action_value = 0
        self.p1.calculate_equipment(level)
        self.p2.calculate_equipment(level)
        self.p3.calculate_equipment(level)

        # Renaming duplicates
        if self.p2.name == self.p1.name:
            self.p2.name += "②"
            if self.p3.name == self.p1.name:
                self.p3.name += "③"
        if self.p3.name == self.p1.name:
            self.p3.name += "②"
        elif self.p3.name == self.p2.name:
            self.p3.name += "②"

        if self.e2.name == self.e1.name:
            self.e2.name += "②"
            if self.e3.name == self.e1.name:
                self.e3.name += "③"
        if self.e3.name == self.e1.name:
            self.e3.name += "②"
        elif self.e3.name == self.e2.name:
            self.e3.name += "②"

    def calculate_turn(self):
        # Calculate speed
        actions = []
        someones_turn = False
        while not someones_turn:
            self.action_value += 1
            for character in self.characters:
                if self.action_value == character.next_action:
                    actions.append(character)
                    someones_turn = True
        return actions

    def check_death(self):
        # Reset negative speeds
        for alive_check in self.player_team:
            if alive_check.speed < 0:
                alive_check.speed = 0
            if alive_check.hp <= 0:
                print(f"{alive_check.name} is dead!")
                self.characters.remove(alive_check)
                self.player_team.remove(alive_check)
        if not self.player_team:
            result = "Lose"
            return result
        for alive_check in self.enemy_team:
            if alive_check.hp <= 0:
                print(f"{alive_check.name} is dead!")
                self.characters.remove(alive_check)
                self.enemy_team.remove(alive_check)
        if not self.enemy_team:
            result = "Win"
            return result
        return None

    def turn(self, character):
        # Determine if character taking turn is ally or enemy
        turn_type = character.__class__.__name__
        # Reset target (IDE keeps showing warnings that I don't like)
        target = None # Used if target is on opposite team
        friend = None # Used if target is on same team
        if character in self.characters:
            time.sleep(1)
            printing_team_list = []
            if turn_type == "Ally":
                # Print current battle, with the character taking turn in the middle
                for e in self.enemy_team:
                    printing_team_list.append(f"{e.name} {str(e.hp)} HP")
                print(", ".join(printing_team_list))
                printing_team_list = []
                print(f"\n            {character.name}")
                print(f"            {str(character.hp)} HP\n")
                for a in self.player_team:
                    if a != character:
                        printing_team_list.append(f"{a.name} {str(a.hp)} HP")
                print(", ".join(printing_team_list))
                print("----------------------------------------------------------------------------------")
                # Player's turn
                print(f"Choose {character.name}'s move:")
                print(f"(1) Normal Attack: {character.normal_name} | (2) Skill: {character.skill_name}")
                attack_option = input()
                while attack_option not in ("1", "2"):
                    print("Invalid input! Select one of the numbers!")
                    print(f"Choose {character.name}'s move:")
                    print(f"(1) Normal Attack: {character.normal_name} | (2) Skill: {character.skill_name}")
                    attack_option = input()
                selected_target = False
                if attack_option == "1":
                    while not selected_target:
                        print("Who will you attack?")
                        print_potential_targets(self.enemy_team)
                        try:
                            target = self.enemy_team[int(input()) - 1]
                            selected_target = True
                        except IndexError:
                            print("Invalid input! Pick a target that's actually alive!")
                            time.sleep(1)
                        except ValueError:
                            print("Invalid input! Please select a number!")
                            time.sleep(1)
                    time.sleep(1)
                    print("----------------------------------------------------------------------------------")
                    damage, crit_display = character.normal()
                    target.lose_health(damage)
                    print(f"{character.name} used {character.normal_name} on {target.name}.")
                    if crit_display:
                        print(f"Dealt {damage} (CRITICAL HIT!) damage.")
                    else:
                        print(f"Dealt {damage} damage.")

                elif attack_option == "2":
                    # Unique skills of each character
                    # Mercenary
                    if character.skill_name == "Motivated Charge":
                        while not selected_target:
                            print("Who will you attack?")
                            print_potential_targets(self.enemy_team)
                            try:
                                target = self.enemy_team[int(input()) - 1]
                                selected_target = True
                            except IndexError:
                                print("Invalid input! Pick a target that's actually alive!")
                            except ValueError:
                                print("Invalid input! Please select a number!")
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        damage, crit_display = character.skill_motivated_charge()
                        target.lose_health(damage)
                        print(f"{character.name} used {character.skill_name} on {target.name}.")
                        if crit_display:
                            print(f"Dealt {damage} (CRITICAL HIT!) damage.")
                        else:
                            print(f"Dealt {damage} damage.")

                    # Adventurer
                    elif character.skill_name == "With All Our Might":
                        while not selected_target:
                            print("Who will you attack?")
                            print_potential_targets(self.enemy_team)
                            try:
                                target = self.enemy_team[int(input()) - 1]
                                selected_target = True
                            except IndexError:
                                print("Invalid input! Pick a target that's actually alive!")
                            except ValueError:
                                print("Invalid input! Please select a number!")
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        damage, crit_display = character.skill_with_all_our_might()
                        target.lose_health(damage)
                        print(f"{character.name} used {character.skill_name} on {target.name}.")
                        if crit_display:
                            print(f"Dealt {damage} (CRITICAL HIT!) damage.")
                        else:
                            print(f"Dealt {damage} damage.")

                    # Fire Wizard
                    elif character.skill_name == "Meteor Shower":
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        for target in self.enemy_team:
                            damage, crit_display = character.skill_meteor_shower()
                            target.lose_health(damage)
                            print(f"{character.name} used {character.skill_name} on {target.name}.")
                            if random.random() < 0.5:
                                target.negative_effects["Burned"] = 3
                                print(f"{target.name} is now burned for 3 turns.")
                            if crit_display:
                                print(f"Dealt {damage} (CRITICAL HIT!) damage.")
                            else:
                                print(f"Dealt {damage} damage.")

                    # Ice Wizard
                    elif character.skill_name == "Icicle Shower":
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        for target in self.enemy_team:
                            damage, crit_display = character.skill_icicle_shower()
                            target.lose_health(damage)
                            print(f"{character.name} used {character.skill_name} on {target.name}.")
                            if random.random() < 0.25:
                                target.negative_effects["Frozen"] = 1
                                print(f"{target.name} is now frozen.")
                            if crit_display:
                                print(f"Dealt {damage} (CRITICAL HIT!) damage.")
                            else:
                                print(f"Dealt {damage} damage.")

                    # Knight
                    elif character.skill_name == "Team Defence":
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        for friend in self.player_team:
                            friend.base_hp += 25
                            friend.hp += 25
                        print(f"{character.name} used {character.skill_name} on your team.")
                        print("Increased HP and base HP of entire team by 25 HP.")

                    # Alchemist
                    elif character.skill_name == "Intense Energy Potion":
                        while not selected_target:
                            print("Who will you support?")
                            print_potential_targets(self.player_team)
                            try:
                                friend = self.player_team[int(input()) - 1]
                                selected_target = True
                            except IndexError:
                                print("Invalid input! Pick a target that's actually alive!")
                            except ValueError:
                                print("Invalid input! Please select a number!")
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        friend.positive_effects["Alchemist Potion"] = 3
                        print(f"{character.name} used {character.skill_name} on {friend.name}.")
                        print(f"Increased CRIT, ATK and SPEED of {friend.name} by 15% for 3 turns.")

                    # Ninja
                    elif character.skill_name == "Sneak":
                        while not selected_target:
                            print("Who will you attack?")
                            print_potential_targets(self.enemy_team)
                            try:
                                target = self.enemy_team[int(input()) - 1]
                                selected_target = True
                            except IndexError:
                                print("Invalid input! Pick a target that's actually alive!")
                            except ValueError:
                                print("Invalid input! Please select a number!")
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        damage, crit_display = character.skill_sneak()
                        target.lose_health(damage)
                        print(f"{character.name} used {character.skill_name} on {target.name}.")
                        if crit_display:
                            print(f"Dealt {damage} (CRITICAL HIT!) damage.")
                        else:
                            print(f"Dealt {damage} damage.")
                        character.base_speed += 20
                        character.speed += 20
                        print(f"Increased {character.name}'s SPEED by 20.")

                    # Wumpus
                    elif character.skill_name == "In Honour of Harry":
                        while not selected_target:
                            print("Who will you attack?")
                            print_potential_targets(self.enemy_team)
                            try:
                                target = self.enemy_team[int(input()) - 1]
                                selected_target = True
                            except IndexError:
                                print("Invalid input! Pick a target that's actually alive!")
                            except ValueError:
                                print("Invalid input! Please select a number!")
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        damage, crit_display = character.skill_in_honour_of_harry()
                        target.lose_health(damage)
                        print(f"{character.name} used {character.skill_name} on {target.name}.")
                        if crit_display:
                            print(f"Dealt {damage} (CRITICAL HIT!) damage.")
                        else:
                            print(f"Dealt {damage} damage.")

                    # Demolitionist
                    elif character.skill_name == "3 Big Booms":
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        for target in self.enemy_team:
                            damage, crit_display = character.skill_big_booms()
                            target.lose_health(damage)
                            print(f"{character.name} used {character.skill_name} on {target.name}.")
                            if crit_display:
                                print(f"Dealt {damage} (CRITICAL HIT!) damage.")
                            else:
                                print(f"Dealt {damage} damage.")

                    # Commander
                    elif character.skill_name == "Depart And Defend":
                        while not selected_target:
                            print("Who will you support?")
                            print_potential_targets(self.player_team)
                            try:
                                friend = self.player_team[int(input()) - 1]
                                selected_target = True
                            except IndexError:
                                print("Invalid input! Pick a target that's actually alive!")
                            except ValueError:
                                print("Invalid input! Please select a number!")
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        friend.positive_effects["Commanded"] = 3
                        print(f"{character.name} used {character.skill_name} on {friend.name}.")
                        print(f"Increased CRIT of {friend.name} by 30% and ATK by 50% for 3 turns.")

                    # Nurse
                    elif character.skill_name == "Heal":
                        while not selected_target:
                            print("Who will you heal?")
                            print_potential_targets(self.player_team)
                            try:
                                friend = self.player_team[int(input()) - 1]
                                selected_target = True
                            except IndexError:
                                print("Invalid input! Pick a target that's actually alive!")
                            except ValueError:
                                print("Invalid input! Please select a number!")
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        heal_amount = round(character.base_hp / 4)
                        print(f"{character.name} used {character.skill_name} on {friend.name}.")
                        friend.hp += heal_amount
                        if friend.hp >= friend.base_hp:
                            friend.hp = friend.base_hp
                            print(f"{friend.name} is now on full health.")
                        else:
                            print(f"Increased HP of {friend.name} by {heal_amount}.")
                        friend.negative_effects = {}
                        print(f"Removed all negative effects from {friend.name}.")

                    # Sorcerer
                    elif character.skill_name == "Dark Magic":
                        while not selected_target:
                            print("Who will you attack?")
                            print_potential_targets(self.enemy_team)
                            try:
                                target = self.enemy_team[int(input()) - 1]
                                selected_target = True
                            except IndexError:
                                print("Invalid input! Pick a target that's actually alive!")
                            except ValueError:
                                print("Invalid input! Please select a number!")
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        damage, crit_display = character.skill_dark_magic_spell()
                        target.lose_health(damage)
                        print(f"{character.name} used {character.skill_name} on {target.name}.")
                        if crit_display:
                            print(f"Dealt {damage} (CRITICAL HIT!) damage.")
                        else:
                            print(f"Dealt {damage} damage.")
                        if random.random() < 0.3:
                            target.negative_effects["Burned"] = 3
                            print(f"{target.name} is now burned for 3 turns.")
                        if random.random() < 0.3:
                            target.negative_effects["Poisoned"] = 3
                            print(f"{target.name} is now poisoned for 3 turns.")
                        if random.random() < 0.3:
                            target.negative_effects["Bleeding"] = 2
                            print(f"{target.name} is now bleeding for 2 turns.")
                        if random.random() < 0.3:
                            target.negative_effects["Slow"] = 2
                            print(f"{target.name} is now slowed for 2 turns.")
                        if random.random() < 0.3:
                            target.negative_effects["Decay"] = 3
                            print(f"{target.name} is now decaying for 3 turns.")

                    # Cleric
                    elif character.skill_name == "Holy Teachings":
                        while not selected_target:
                            print("Who will you support?")
                            print_potential_targets(self.player_team)
                            try:
                                friend = self.player_team[int(input()) - 1]
                                selected_target = True
                            except IndexError:
                                print("Invalid input! Pick a target that's actually alive!")
                            except ValueError:
                                print("Invalid input! Please select a number!")
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        friend.positive_effects["Cleric's Faith"] = 2
                        print(f"{character.name} used {character.skill_name} on {friend.name}.")
                        print(f"Increased ATK of {friend.name} by 60% and SPEED by 10% for 2 turns.")

                    # End unique skills of each character
                    decreased_speed = round(character.base_speed / 20)
                    character.base_speed -= decreased_speed
                    character.speed -= decreased_speed
                    time.sleep(1)
                    print(f"Due to skill usage, {character.name}'s SPEED decreases by {decreased_speed}.")
                    print(f"New SPEED of {character.name}: {character.speed}")


            elif turn_type == "Enemy":
                # Enemy turn, completely automated
                for e in self.enemy_team:
                    if e != character:
                        printing_team_list.append(f"{e.name} {str(e.hp)} HP")
                print(", ".join(printing_team_list))
                printing_team_list = []
                print(f"\n            {character.name}")
                print(f"            {str(character.hp)} HP\n")
                for a in self.player_team:
                    printing_team_list.append(f"{a.name} {str(a.hp)} HP")
                print(", ".join(printing_team_list))
                print("----------------------------------------------------------------------------------")

                # Check if enemy has custom AI
                # For custom AI, always use normal_name and not name
                # Boss fights:
                if character.normal_name == "honey squirts":
                    character.attack_sequence += 1
                    if character.attack_sequence == 4:
                        character.attack_sequence = 1
                    if character.attack_sequence == 1:
                        bee_summons = 3 - len(self.enemy_team)
                        for _ in range(bee_summons):
                            print("The Queen BEE (BOSS) spawns a Little Bee")
                            bee = fighter.Enemy("Little Bee", 0)
                            bee.next_action = self.action_value + round(10000 / character.speed)
                            self.enemy_team.append(bee)
                    elif character.attack_sequence == 2:
                        for target in self.enemy_team:
                            damage = character.normal()
                            target.lose_health(damage)
                            print(f"{character.name} honey squirts {target.name}.")
                            print(f"Dealt {damage} damage.")
                            if random.random() < 0.3:
                                target.negative_effects["Slow"] = 2
                                print(f"{character.normal_name} is slow for the next 2 turns.")
                    elif character.attack_sequence == 3:
                        target = random.choice(self.player_team)
                        damage = character.normal() * 2
                        target.lose_health(damage)
                        print(f"{character.name} ruthlessly stings {target.name}.")
                        print(f"Dealt {damage} damage.")
                elif character.normal_name == "fireballs":
                    character.attack_sequence += 1
                    if character.attack_sequence == 4:
                        character.attack_sequence = 1
                    if character.attack_sequence == 1:
                        character.hp += 100
                        character.atk += round(character.atk / 10)
                        print("The Hell-Infused Dragon (BOSS) dances!" )
                        print("Its health is increased by 100 HP!")
                        print("Its attack is increased by 10%!")
                        for target in self.enemy_team:
                            if random.random() < 0.3:
                                target.negative_effects["Grief"] = 3
                                print(f"{target.normal_name} is having some mental difficulties for the next 3 turns.")
                    elif character.attack_sequence == 2:
                        for target in self.enemy_team:
                            damage = character.normal()
                            target.lose_health(damage)
                            print(f"{character.name} breathes fire at {target.name}.")
                            print(f"Dealt {damage} damage.")
                            target.negative_effects["Burn"] = 2
                            print(f"{target.normal_name} is now burned for the next 2 turns.")
                    elif character.attack_sequence == 3:
                        for _ in range(5):
                            target = random.choice(self.player_team)
                            damage = round(character.normal() * 0.6)
                            target.lose_health(damage)
                            print(f"{character.name} swoops into {target.name}.")
                            print(f"Dealt {damage} damage.")
                else:
                    # Regular damage
                    target = random.choice(self.player_team)
                    damage = character.normal()
                    target.lose_health(damage)
                    print(f"{character.name} {character.normal_name} {target.name}.")
                    print(f"Dealt {damage} damage.")
                    # Attacks that apply effects
                    if character.normal_name == "poisons" or character.normal_name == "stings":
                        target.negative_effects["Poisoned"] = 3
                        print(f"{target.normal_name} is poisoned for the next 3 turns.")
                    elif character.normal_name == "swoops down on" or character.normal_name == "viciously bites":
                        target.negative_effects["Bleeding"] = 2
                        print(f"{target.normal_name} is bleeding for the next 2 turns.")
                    elif character.normal_name == "ambushes":
                        if random.random() < 0.5:
                            target.negative_effects["Slow"] = 2
                            print(f"{target.normal_name} is slow for the next 2 turns.")
                    elif character.normal_name == "torments":
                        if random.random() < 0.3:
                            target.negative_effects["Grief"] = 3
                            print(f"{target.normal_name} is having some mental difficulties for the next 3 turns.")
            try:
                character.next_action += round(10000 / character.speed)
            except ZeroDivisionError:
                character.next_action = -1
            time.sleep(1)
            print("----------------------------------------------------------------------------------")
