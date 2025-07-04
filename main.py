import time, random

version = "v1.0.11"
last_update = "04/07/2025"

level = 0
level_up_requirement = 0
xp = 0
coins = 0
dead = False

inventory = {"Stick": 1,
             "Cloth Robe": 1}
owned_character_list = []

biomes = ("Cave Entrance", "Gemstone Geodes", "Abandoned Mines", "Mossy Caves", "Deep Caverns", "Underworld", "Dungeons")
unlocked_biomes = ["Cave Entrance"]
current_biome = "Cave Entrance"

def load():
    with open("ally.txt", "r") as allies:
        allies_dict = {}
        for ally in allies:
            ally_list = ally.strip().split("|")
            allies_dict[ally_list[0]] = [ally_list[1], int(ally_list[2]), int(ally_list[3]), int(ally_list[4]),
                                         ally_list[5], int(ally_list[6]), ally_list[7], ally_list[8], ally_list[9]]
        # Structure of ally.txt: Name|Role|Base HP|Base ATK|Base SPEED|
        #                        Normal Attack Name|Damage %|Normal Attack Description|Skill Name|Skill Description

    with open("enemy.txt", "r") as enemies:
        enemies_dict = {}
        for enemy in enemies:
            enemy_list = enemy.strip().split("|")
            enemies_dict[enemy_list[0]] = [int(enemy_list[1]), int(enemy_list[2]), int(enemy_list[3]),
                                           int(enemy_list[4]), enemy_list[5], enemy_list[6], int(enemy_list[7])]
        # Structure of enemy.txt: Name|Biome Number|Base HP|Base ATK|
        #                         Base SPEED|Rarity|Normal Attack Name|Damage %

    with open("gear.txt", "r") as gears:
        weapon_dict = {}
        armour_dict = {}
        for gear in gears:
            gear_list = gear.strip().split("|")
            if gear_list[1] == "Weapon":
                weapon_dict[gear_list[0]] = [gear_list[2], int(gear_list[3]), int(gear_list[4]), gear_list[5]]
            elif gear_list[1] == "Armour":
                armour_dict[gear_list[0]] = [gear_list[2], int(gear_list[3]), int(gear_list[4]), gear_list[5]]
        # Structure of gear.txt: Name|Type|Rarity|HP/ATK|Level Requirement|Notes

    with open("items.txt", "r") as items:
        items_dict = {}
        for item in items:
            item_list = item.strip().split("|")
            items_dict[item_list[0]] = [item_list[1], item_list[2], int(item_list[3]), item_list[4]]
        # Structure of items.txt: Name|Type|Rarity|Level Requirement|Notes
        # Weapons and armour are NOT item objects

    return allies_dict, enemies_dict, weapon_dict, armour_dict, items_dict


def find_enemy(biome_no, enemy_rarity, enemies_dict):
    for key_enemy, value_enemy in enemies_dict.items():
        if value_enemy[0] == biome_no and value_enemy[4] == enemy_rarity:
            return key_enemy
    print("Error: enemy.txt is missing or malformed!")
    print("Press any key to close the program.")
    raise SystemExit


# Start game
print("----------------------------------------------------------------------------------")
print(f"Cavern Clash {version}")
print(f"Last update: {last_update}")
print("Please wait while we load the game.")
print("If this takes a long time, then the game will not run smoothly.")
import battle, shop, fighter
all_allies, all_enemies, all_weapons, all_armour, all_items = load()
current_team = [fighter.Ally("Adventurer", level), fighter.Ally("Adventurer", level), fighter.Ally("Adventurer", level)]
store = shop.Shop()
print("Game loaded successfully.")
name = input("Begin by entering your name: ")
time.sleep(1)
print("----------------------------------------------------------------------------------")
print(f"Welcome to Cavern Clash, {name}!")
print(f"Would you like to play through the tutorial?")
print("(1) Yes | (2) No")
tutorial_query = input()
if tutorial_query == "1":
    time.sleep(1)
    print("----------------------------------------------------------------------------------")
    p1 = fighter.Ally("Mercenary", level)
    p2 = fighter.Ally("Mercenary", level)
    p3 = fighter.Ally("Mercenary", level)
    e1 = fighter.Enemy("Rock", level)
    e2 = fighter.Enemy("Golem", level)
    e3 = fighter.Enemy("Rock", level)
    tutorial = battle.BattleManager([p1, p2, p3, e1, e2, e3], 0)
    result = None
    while not result:
        result = tutorial.check_death()
        actions = tutorial.calculate_turn()
        for guy in actions:
            guy.apply_effects()
            result = tutorial.check_death()
            if result:
                break
            if guy in tutorial.characters:
                tutorial.turn(guy)

result = None
while not result:
    time.sleep(1)
    print("----------------------------------------------------------------------------------")
    print(f"Your current location: {current_biome}")
    print("Action Select:")
    print("(1) Explore | (2) Inventory and Crafting | (3) Team Configuration | (4) Shop")
    location = biomes.index(current_biome)
    if location == 0:
        print(f"(R / Right) Travel to {biomes[location + 1]}")
    elif location == 5:
        print(f"(L / Left) Travel to {biomes[location - 1]} | (R / Right) Travel to {biomes[location + 1]}")
        # Dungeon confirmation message
    else:
        print(f"(L / Left) Travel to {biomes[location - 1]} | (R / Right) Travel to {biomes[location + 1]}")
    move = input()
    time.sleep(1)
    print("----------------------------------------------------------------------------------")
    if move == "1":
        if len(current_team) != 3:
            print("Sorry, you need 3 characters on your team to go exploring.")
            print("You can manage your characters in the Team Configuration (3)")
        else:
            print(f"Exploring the {current_biome}...")
            characters = []
            for player_character in current_team:
                characters.append(player_character)
            biome_number = biomes.index(current_biome)
            normal_enemy = find_enemy(biome_number, "Normal", all_enemies)
            rare_enemy = find_enemy(biome_number, "Rare", all_enemies)
            legendary_enemy = find_enemy(biome_number, "Legendary", all_enemies)
            reward_score = 1
            win_chance = False
            for enemy_selection in range(3):
                enemy_roll = random.random()
                if enemy_roll <= (0.7 - 0.05 * biome_number):
                    characters.append(fighter.Enemy(normal_enemy, level))
                    reward_score += 1
                elif enemy_roll <= (0.99 - 0.02 * biome_number):
                    characters.append(fighter.Enemy(rare_enemy, level))
                    reward_score += 3
                else:
                    characters.append(fighter.Enemy(legendary_enemy, level))
                    reward_score += 10
                    if legendary_enemy == "Hell-Infused Dragon (BOSS)":
                        win_chance = True
            encounter = battle.BattleManager(characters, level)
            result = None
            while not result:
                result = encounter.check_death()
                actions = encounter.calculate_turn()
                for guy in actions:
                    guy.apply_effects()
                    result = encounter.check_death()
                    if result:
                        break
                    if guy in encounter.characters:
                        encounter.turn(guy)
            if result == "Win":
                time.sleep(1)
                print("----------------------------------------------------------------------------------")
                print("Congratulations, you have survived another battle!")
                # Rewards
                final_reward_score = random.randint(4, reward_score + 1)
                # Range of final_reward_score: 4 to 31
                # However as legendary enemies are really rare, final_reward_score usually lies between 4 and 10
                reward_coins = 10 * reward_score * (biome_number + 1) * 2
                # Doubled coin reward until materials are introduced
                coins += reward_coins
                reward_xp = 5 * (biome_number + 1) + random.randint(-3, 3)
                reward_xp += reward_score - 4
                xp += reward_xp
                print("Rewards:")
                print(f"+{reward_coins} coins")
                print(f"+{reward_xp} score")
                # Lootbox drop
                if final_reward_score >= random.randint(5, 15):
                    quantity_owned = inventory.get("Character Lootbox")
                    if quantity_owned is None:
                        quantity_owned = 0
                    quantity_owned += 1
                    inventory["Character Lootbox"] = quantity_owned
                    print("+1 Character Lootbox")

                if final_reward_score >= random.randint(4, 12):
                    quantity_owned = inventory.get("Weapon Lootbox")
                    if quantity_owned is None:
                        quantity_owned = 0
                    quantity_owned += 1
                    inventory["Weapon Lootbox"] = quantity_owned
                    print("+1 Weapon Lootbox")

                if final_reward_score >= random.randint(4, 12):
                    quantity_owned = inventory.get("Armour Lootbox")
                    if quantity_owned is None:
                        quantity_owned = 0
                    quantity_owned += 1
                    inventory["Armour Lootbox"] = quantity_owned
                    print("+1 Armour Lootbox")

                if final_reward_score >= random.randint(4, 12):
                    quantity_owned = inventory.get("Item Lootbox")
                    if quantity_owned is None:
                        quantity_owned = 0
                    amount = random.randint(1, 6)
                    quantity_owned += amount
                    inventory["Item Lootbox"] = quantity_owned
                    print(f"+{amount} Item Lootbox")

                while xp >= level_up_requirement:
                    level += 1
                    level_up_requirement += 10 * level
                    print(f"Level up! {level - 1} -> {level}")
                    print(f"Base HP of all characters +1")
                    if level == 1:
                        print("New feature unlocked: Shop")
                        store.restock(level)
                        store.restock_attempts = 1
                    elif level == 3:
                        print("New area unlocked: Gemstone Geodes")
                        unlocked_biomes.append("Gemstone Geodes")
                    elif level == 5:
                        print("New feature unlocked: Refinement stones")
                        print("Refinement stones can be used further improve the effect of weapons and armour.")
                    elif level == 7:
                        print("New feature unlocked: Extra shop slot (1/3)")
                        store.slots += 1
                    elif level == 8:
                        print("New area unlocked: Abandoned Mines")
                        unlocked_biomes.append("Abandoned Mines")
                    # elif level == 10:
                        # print("New feature unlocked: Selling weapons and armour")
                        # print("Your unneeded gear can now be sold for extra coins.")
                        # store.buy_gear = True
                    elif level == 15:
                        print("New area unlocked: Mossy Caves")
                        unlocked_biomes.append("Mossy Caves")
                    elif level == 20:
                        print("New feature unlocked: Extra shop slot (2/3)")
                        store.slots += 1
                    # Deep Caverns unlocks via bossfight, but the game ends here for now
                    elif level >= 30 and "Deep Caverns" in unlocked_biomes and "Underworld" not in unlocked_biomes:
                        print("New area unlocked: Underworld")
                        print("New feature unlocked: Extra shop slot (3/3)")
                        store.slots += 1
                        unlocked_biomes.append("Underworld")
                    # Ancient Dungeons unlocks via bossfight
                print(f"For your next level up, you will need {level_up_requirement - xp} more score.")
                store.restock_attempts = 1
                if win_chance:
                    print("----------------------------------------------------------------------------------")
                    print("The Hell-Infused Dragon lays at your feet.")
                    print("Smoke no longer erupts from his nostrils.")
                    print("Congratulations, you have beaten the game!")
                    print("Thank you for playing Cavern Clash!")
                result = None
    elif move == "2":
        left = False
        while not left:
            print("Inventory")
            print(f"Coins: {coins}")
            print(f"Score: {xp}")
            print(f"Level: {level}")
            print(f"Required score to level up: {level_up_requirement}")
            print("Action Select:")
            print("Warning: Viewing your entire inventory will output a lot of information!")
            print("(1) View Specific Item | (2) View Entire Inventory | (3) Open a lootbox | (4) Exit")
            inv_action = input()
            if inv_action == "1":
                time.sleep(1)
                print("----------------------------------------------------------------------------------")
                print("Please type the name of the item you would like to view.")
                inventory_query = input().title()
                weapon_info = all_weapons.get(inventory_query)
                if weapon_info:
                    print(inventory_query)
                    print(f"Type: {weapon_info[0].upper()} Weapon")
                    print(f"Required level: {weapon_info[2]}")
                    print(weapon_info[3])
                armour_info = all_armour.get(inventory_query)
                if armour_info:
                    print(inventory_query)
                    print(f"Type: {armour_info[0].upper()} Armour")
                    print(f"Required level: {armour_info[2]}")
                    print(armour_info[3])
                item_info = all_items.get(inventory_query)
                if item_info:
                    print(inventory_query)
                    print(f"Type: {item_info[1].upper()} {item_info[0]}")
                    print(f"Required level: {item_info[2]}")
                    print(item_info[3])
                print(f"Quantity owned: {inventory.get(inventory_query)}")
                time.sleep(1)
                print("----------------------------------------------------------------------------------")
            elif inv_action == "2":
                inventory = dict(sorted(inventory.items()))
                inventory_weapons = {}
                inventory_armour = {}
                inventory_refine = {}
                inventory_lootbox = {}
                inventory_material = {}
                for key_inventory, value_inventory in inventory.items():
                    if key_inventory in all_weapons:
                        inventory_weapons[key_inventory] = value_inventory
                    elif key_inventory in all_armour:
                        inventory_armour[key_inventory] = value_inventory
                    elif all_items[key_inventory][0] == "Refine":
                        inventory_refine[key_inventory] = value_inventory
                    elif all_items[key_inventory][0] == "Lootbox":
                        inventory_lootbox[key_inventory] = value_inventory
                    elif all_items[key_inventory][0] == "Material":
                        inventory_material[key_inventory] = value_inventory
                print("----------------------------------------------------------------------------------")
                print("WEAPONS")
                for key_inventory, value_inventory in inventory_weapons.items():
                    print(f"{key_inventory} - {value_inventory}")
                print("ARMOUR")
                for key_inventory, value_inventory in inventory_armour.items():
                    print(f"{key_inventory} - {value_inventory}")
                print("REFINEMENT STONES")
                for key_inventory, value_inventory in inventory_refine.items():
                    print(f"{key_inventory} - {value_inventory}")
                print("LOOTBOXES")
                for key_inventory, value_inventory in inventory_lootbox.items():
                    print(f"{key_inventory} - {value_inventory}")
                print("MATERIALS")
                for key_inventory, value_inventory in inventory_material.items():
                    print(f"{key_inventory} - {value_inventory}")
                time.sleep(1)
                print("----------------------------------------------------------------------------------")
            elif inv_action == "3":
                inventory_lootbox = {}
                print("Your lootboxes:")
                for key_inventory, value_inventory in inventory.items():
                    if "Lootbox" in key_inventory:
                        inventory_lootbox[key_inventory] = value_inventory
                for key_inventory, value_inventory in inventory_lootbox.items():
                    print(f"{key_inventory} - {value_inventory}")
                print("What lootbox would you like to open? (Type name)")
                lootbox = input().title()
                if lootbox == "Character" or lootbox == "Character Lootbox":
                    lootbox = "Character Lootbox"
                elif lootbox == "Weapon" or lootbox == "Weapon Lootbox":
                    lootbox = "Weapon Lootbox"
                elif lootbox == "Armour" or lootbox == "Armour Lootbox":
                    lootbox = "Armour Lootbox"
                elif lootbox == "Item" or lootbox == "Item Lootbox":
                    lootbox = "Item Lootbox"
                elif lootbox == "Coin" or lootbox == "Coin Lootbox":
                    lootbox = "Coin Lootbox"
                else:
                    lootbox = "Not a lootbox"
                # If the chosen lootbox is in inventory
                if inventory_lootbox.get(lootbox):
                    print("How many would you like to open? (Type amount) | (A) All")
                    amount_to_open = input().title()
                    if amount_to_open == "A" or amount_to_open == "All":
                        amount_to_open = inventory_lootbox.get(lootbox)
                    amount_to_open = int(amount_to_open)
                    if amount_to_open > 0:
                        try:
                            amount_to_open = int(amount_to_open)
                            if amount_to_open >= inventory_lootbox.get(lootbox):
                                inventory_lootbox[lootbox] -= amount_to_open
                                if inventory_lootbox[lootbox] <= 0:
                                    del inventory_lootbox[lootbox]
                                if lootbox == "Character Lootbox":
                                    for o in range(amount_to_open):
                                        new_character = random.choice(list(all_allies.keys()))
                                        owned_character_list.append(fighter.Ally(new_character, level))
                                        print(f"Received {new_character} (Character)")
                                elif lootbox == "Weapon Lootbox":
                                    unlocked_weapons = []
                                    for key_weapon, value_weapon in all_weapons.items():
                                        if value_weapon[2] <= level:
                                            unlocked_weapons.append(key_weapon)
                                    for o in range(amount_to_open):
                                        new_weapon = random.choice(unlocked_weapons)
                                        quantity_owned = inventory.get(new_weapon)
                                        if quantity_owned is None:
                                            quantity_owned = 0
                                        quantity_owned += 1
                                        inventory[new_weapon] = quantity_owned
                                        print(f"Received {new_weapon} (Weapon)")
                                elif lootbox == "Armour Lootbox":
                                    unlocked_armour = []
                                    for key_armour, value_armour in all_armour.items():
                                        if value_armour[2] <= level:
                                            unlocked_armour.append(key_armour)
                                    for o in range(amount_to_open):
                                        new_armour = random.choice(unlocked_armour)
                                        quantity_owned = inventory.get(new_armour)
                                        if quantity_owned is None:
                                            quantity_owned = 0
                                        quantity_owned += 1
                                        inventory[new_armour] = quantity_owned
                                        print(f"Received {new_armour} (Armour)")
                                elif lootbox == "Item Lootbox":
                                    unlocked_items = []
                                    for key_item, value_item in all_items.items():
                                        if value_item[2] <= level:
                                            unlocked_items.append(key_item)
                                    for o in range(amount_to_open):
                                        new_item = random.choice(unlocked_items)
                                        quantity_owned = inventory.get(new_item)
                                        if quantity_owned is None:
                                            quantity_owned = 0
                                        quantity_owned += 1
                                        inventory[new_item] = quantity_owned
                                        print(f"Received {new_item} (Item)")
                                elif lootbox == "Coin Lootbox":
                                    for o in range(amount_to_open):
                                        new_coins = 10 * (level + 1) + random.randint(-5, 5)
                                        coins += new_coins
                                        print(f"+{new_coins} coins")
                                for r in range(amount_to_open):
                                    inventory[lootbox] -= 1
                                    if inventory.get(lootbox) <= 0:
                                        del inventory[lootbox]
                            else:
                                print("Invalid input! You do not have that many lootboxes in your inventory!")
                        except ValueError:
                            print("Invalid input! Enter a number, or type 'A' for all!")
                    else:
                        print("Invalid input! You don't have that many lootboxes to open!")
                else:
                    print("Invalid input! You don't have any of that lootbox!")
                time.sleep(1)
                print("----------------------------------------------------------------------------------")


            # elif inv_action == "4":
                # Crafting will be introduced later
            else:
                left = True
    elif move == "3":
        left = False
        while not left:
            print("Team Configuration")
            inventory = dict(sorted(inventory.items()))
            inventory_weapons = {}
            inventory_armour = {}
            inventory_refine = {}
            for key_inventory, value_inventory in inventory.items():
                if key_inventory in all_weapons:
                    inventory_weapons[key_inventory] = value_inventory
                elif key_inventory in all_armour:
                    inventory_armour[key_inventory] = value_inventory
                elif all_items[key_inventory][0] == "Refine":
                    inventory_refine[key_inventory] = value_inventory
            # Printing character information
            for d in range(3):
                display = current_team[d]
                display.calculate_equipment(level)
                print(f"({d + 1}) {display.name} | Base HP: {display.base_hp}, Base ATK: {display.base_atk}, "
                      f"Base SPEED: {display.base_speed}")
                print(f"Weapon: {display.weapon} | Stone: {display.weapon_stone}")
                print(f"Armour: {display.armour} | Stone: {display.armour_stone}")
                print(f"Normal attack - {display.normal_name}: {display.normal_description}")
                print(f"Skill - {display.skill_name}:")
                print(display.skill_description)
            print("(1) Manage character equipment | (2) Replace character | (3) Exit")
            config_action = input()
            if config_action == "1":
                print("----------------------------------------------------------------------------------")
                print("What character would you like to change the equipment for?")
                print(f"(1) {current_team[0].name} | (2) {current_team[1].name} | (3) {current_team[2].name}")
                try:
                    managing_character = current_team[int(input()) - 1]
                    print("What would you like to equip/unequip?")
                    print("(1) Weapon | (2) Armour | (3) Weapon Stone | (4) Armour Stone | (5) Cancel")
                    equipment_slot = input()
                    if equipment_slot == "1":
                        if managing_character.weapon:
                            print(f"Unequipping {managing_character.weapon}...")
                            if managing_character.weapon in inventory.keys():
                                inventory[managing_character.weapon] += 1
                            else:
                                inventory[managing_character.weapon] = 1
                            managing_character.weapon = None
                        print("Inventory - Weapons:")
                        for key_inventory, value_inventory in inventory_weapons.items():
                            print(f"{key_inventory}: {value_inventory}")
                        print(f"What weapon would you like to equip on {managing_character.name}? (Type name)")
                        equip = input().title()
                        if equip in inventory.keys():
                            inventory[equip] -= 1
                            if inventory[equip] == 0:
                                del inventory[equip]
                            managing_character.weapon = equip
                            print(f"{equip} successfully equipped.")
                        else:
                            print("Invalid input! This item is not in your inventory!")

                    elif equipment_slot == "2":
                        if managing_character.armour:
                            print(f"Unequipping {managing_character.armour}...")
                            if managing_character.armour in inventory.keys():
                                inventory[managing_character.armour] += 1
                            else:
                                inventory[managing_character.armour] = 1
                            managing_character.armour = None
                        print("Inventory - Armour:")
                        for key_inventory, value_inventory in inventory_armour.items():
                            print(f"{key_inventory}: {value_inventory}")
                        print(f"What armour would you like to equip on {managing_character.name}? (Type name)")
                        equip = input().title()
                        if equip in inventory.keys():
                            inventory[equip] -= 1
                            if inventory[equip] == 0:
                                del inventory[equip]
                            managing_character.armour = equip
                            print(f"{equip} successfully equipped.")
                        else:
                            print("Invalid input! This item is not in your inventory!")

                    elif equipment_slot == "3":
                        if managing_character.weapon_stone:
                            print(f"Unequipping {managing_character.weapon_stone}...")
                            if managing_character.weapon_stone in inventory.keys():
                                inventory[managing_character.weapon_stone] += 1
                            else:
                                inventory[managing_character.weapon_stone] = 1
                            managing_character.weapon_stone = None
                        print("Inventory - Refinement Stones:")
                        for key_inventory, value_inventory in inventory_refine.items():
                            print(f"{key_inventory}: {value_inventory}")
                        print(f"What armour would you like to equip on {managing_character.name}? (Type name)")
                        equip = input().title()
                        if equip in inventory.keys():
                            inventory[equip] -= 1
                            if inventory[equip] == 0:
                                del inventory[equip]
                            managing_character.weapon_stone = equip
                            print(f"{equip} successfully equipped.")
                        else:
                            print("Invalid input! This item is not in your inventory!")

                    elif equipment_slot == "4":
                        if managing_character.armour_stone:
                            print(f"Unequipping {managing_character.armour_stone}...")
                            if managing_character.armour_stone in inventory.keys():
                                inventory[managing_character.armour_stone] += 1
                            else:
                                inventory[managing_character.armour_stone] = 1
                            managing_character.armour_stone = None
                        print("Inventory - Refinement Stones:")
                        for key_inventory, value_inventory in inventory_refine.items():
                            print(f"{key_inventory}: {value_inventory}")
                        print(f"What armour would you like to equip on {managing_character.name}? (Type name)")
                        equip = input().title()
                        if equip in inventory.keys():
                            inventory[equip] -= 1
                            if inventory[equip] == 0:
                                del inventory[equip]
                            managing_character.armour_stone = equip
                            print(f"{equip} successfully equipped.")
                        else:
                            print("Invalid input! This item is not in your inventory!")
                    else:
                        print("Invalid input! Select the number next to the character!")
                except ValueError:
                    print("Invalid input! Select the corresponding number!")
                except IndexError:
                    print("Invalid input! Select the number next to one of your characters!")
                time.sleep(1)
                print("----------------------------------------------------------------------------------")
            # Switching character
            elif config_action == "2":
                print("----------------------------------------------------------------------------------")
                print("What character would you like to replace?")
                print(f"(1) {current_team[0].name} | (2) {current_team[1].name} | (3) {current_team[2].name}")
                try:
                    replaced_character = current_team[int(input()) - 1]
                    print("Owned characters:")
                    name_character_list = []
                    for owned_character in owned_character_list:
                        name_character_list.append(owned_character.name)
                    sorted_character_list = sorted(name_character_list)
                    print("\n".join(sorted_character_list))
                    print("What character would you like to add to your team? (Type name)")
                    insert_character = input().title()
                    managing_character = None
                    if insert_character in name_character_list:
                        for owned_character in owned_character_list:
                            if owned_character.name == insert_character:
                                managing_character = owned_character
                                owned_character_list.remove(owned_character)
                                break
                        time.sleep(1)
                        print("----------------------------------------------------------------------------------")
                        print(insert_character)
                        managing_character.calculate_equipment(level)
                        print(f"Base HP: {managing_character.base_hp}, Base ATK: {managing_character.base_atk}, "
                              f"Base SPEED: {managing_character.base_speed}")
                        print(f"Normal attack - {managing_character.normal_name}: "
                              f"{managing_character.normal_description}")
                        print(f"Skill - {managing_character.skill_name}:")
                        print(managing_character.skill_description)
                        print(f"Confirm replacement of {replaced_character.name} with {managing_character.name}?")
                        print("(1) Yes | (2) No")
                        confirm = input()
                        if confirm == "1":
                            current_team.insert(current_team.index(replaced_character), managing_character)
                            current_team.remove(replaced_character)
                            print("Replacement successful.")
                            if replaced_character.weapon:
                                if replaced_character.weapon in inventory.keys():
                                    inventory[replaced_character.weapon] += 1
                                else:
                                    inventory[replaced_character.weapon] = 1
                                replaced_character.weapon = None

                            if replaced_character.armour:
                                if replaced_character.armour in inventory.keys():
                                    inventory[replaced_character.armour] += 1
                                else:
                                    inventory[replaced_character.armour] = 1
                                replaced_character.armour = None

                            if replaced_character.weapon_stone:
                                if replaced_character.weapon_stone in inventory.keys():
                                    inventory[replaced_character.weapon_stone] += 1
                                else:
                                    inventory[replaced_character.weapon_stone] = 1
                                replaced_character.weapon_stone = None

                            if replaced_character.armour_stone:
                                if replaced_character.armour_stone in inventory.keys():
                                    inventory[replaced_character.armour_stone] += 1
                                else:
                                    inventory[replaced_character.armour_stone] = 1
                                replaced_character.armour_stone = None

                            print(f"All items on {replaced_character.name} have been moved to your inventory.")

                        else:
                            print("Replacement cancelled.")
                    else:
                        print("Invalid input! That character is not in your character list!")
                except ValueError:
                    print("Invalid input! Select the corresponding number!")
                except IndexError:
                    print("Invalid input! Select the number next to one of your characters!")
                time.sleep(1)
                print("----------------------------------------------------------------------------------")
            else:
                left = True
    elif move == "4":
        if level == 0:
            print("Sorry, you have not unlocked the shop yet.")
            print("Please come back after reaching level 1.")
        else:
            left = False
            while not left:
                print("Shop")
                print(f"Coins: {coins}")
                print(f"Restock attempts: {store.restock_attempts}")
                print("Current sales:")
                store.display()
                print("Action Select:")
                print("(1) Buy item | (2) Restock | (3) Leave")
                shop_action = input()
                if shop_action == "1":
                    print("Select the number next to the item you want to buy, or anything else to cancel")
                    slot = int(input())
                    try:
                        if slot in range(1, store.slots + 1):
                            if store.check_single(slot):
                                amount = 1
                            else:
                                print("How much of that item would you like to buy?")
                                amount = int(input())
                            time.sleep(1)
                            print("----------------------------------------------------------------------------------")
                            bought_item, price, buy_success = store.buy(slot, coins, amount)
                            if buy_success:
                                coins -= price
                                quantity_owned = inventory.get(bought_item)
                                if quantity_owned is None:
                                    quantity_owned = 0
                                quantity_owned += amount
                                inventory[bought_item] = quantity_owned
                        else:
                            print("Invalid input. Please select a valid amount.")
                    except ValueError:
                        print("Invalid input! Please select the number next to the item you want to buy!")
                    time.sleep(1)
                    print("----------------------------------------------------------------------------------")

                elif shop_action == "2":
                    print("----------------------------------------------------------------------------------")
                    if store.restock_attempts == 1:
                        store.restock(level)
                        print("Shop successfully restocked.")
                    else:
                        print("You have run out of restock attempts.")
                        print("Win another battle to gain a restock attempt.")
                    time.sleep(1)
                    print("----------------------------------------------------------------------------------")
                else:
                    left = True
    elif move.title() == "L" or move.title() == "Left":
        if location > 0:
            current_biome = biomes[location - 1]
            print(f"Moving to {current_biome}...")
            time.sleep(1)
            print("Navigation successful.")
        else:
            print("Invalid input! Theres nothing to the left!")
    elif move.title() == "R" or move.title() == "Right":
        if biomes[location + 1] in unlocked_biomes:
            current_biome = biomes[location + 1]
            print(f"Moving to {current_biome}...")
            time.sleep(1)
            print("Navigation successful.")
        else:
            print(f"Sorry, you have not unlocked {biomes[location + 1]} yet.")
            print("To unlock, keep leveling up, or a specific boss needs to be defeated...")
    else:
        print("Invalid input! Please try again.")

if result == "Lose":
    time.sleep(1)
    print("----------------------------------------------------------------------------------")
    print("Game Over! You have been defeated in battle!")
