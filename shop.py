import random

with open("items.txt", "r") as items:
    items_dict = {}
    for item in items:
        item_list = item.strip().split("|")
        items_dict[item_list[0]] = [item_list[1], item_list[2], int(item_list[3]), item_list[4]]
        # Name|Type|Rarity|Level Requirement|Notes

with open("gear.txt", "r") as gears:
    gear_dict = {}
    for gear in gears:
        gear_list = gear.strip().split("|")
        gear_dict[gear_list[0]] = [gear_list[1] ,gear_list[2], int(gear_list[3]), int(gear_list[4]), gear_list[5]]
    # Structure of gear.txt: Name|Type|Rarity|HP/ATK|Level Requirement|Notes

class Shop:
    # This class is used to manage the shop
    def __init__(self):
        self.selling = {}
        self.unlocked_trades = []
        self.slots = 3
        self.restock_attempts = 0
        self.offer_list = []

    def restock(self, level):
        # Level (integer): Used to determine what items the player has unlocked, to balance the game
        # Generate new trades
        self.selling = {}
        self.restock_attempts -= 1
        for key_item, value_item in items_dict.items():
            if key_item not in self.unlocked_trades:
                if value_item[2] <= level:
                    self.unlocked_trades.append(key_item)
        for key_gear, value_gear in gear_dict.items():
            if key_gear not in self.unlocked_trades:
                if value_gear[3] <= level:
                    self.unlocked_trades.append(key_gear)
        for trade in range(self.slots):
            offer = random.choice(self.unlocked_trades)
            while offer in self.selling.keys():
                offer = random.choice(self.unlocked_trades)
            # If the offer is an item, it will be cheaper and can be sold in a greater quantity.
            offer_details = items_dict.get(offer)
            price = 0
            quantity = 0
            if offer_details: # Items
                item_type = offer_details[0]
                rarity = offer_details[1]
                level_req = offer_details[2] + 1
                description = offer_details[3]
                # Determining price based on rarity and type of item/material
                if rarity == "Normal":
                    quantity = 50
                    price = 5 * level_req
                elif rarity == "Rare":
                    quantity = 20
                    price = 50 * level_req
                elif rarity == "SuperRare":
                    quantity = 10
                    price = 200 * level_req
                elif rarity == "Legendary":
                    quantity = 2
                    price = 1000 * level_req
                if item_type == "Lootbox":
                    quantity = 1
                    price = 50 * level_req
                elif item_type == "Refine":
                    quantity = 1
                    price *= 5

            else: # Weapons and armour cost a lot more
                offer_details = gear_dict.get(offer)
                item_type = offer_details[0]
                rarity = offer_details[1]
                level_req = offer_details[3] + 1
                description = offer_details[4]
                if rarity == "Normal":
                    price = 20 * level_req
                elif rarity == "Rare":
                    price = 200 * level_req
                elif rarity == "SuperRare":
                    price = 1000 * level_req
                elif rarity == "Legendary":
                    price = 5000 * level_req
                quantity = 1 # Only 1 of each weapon and armour can be bought from one trade

            self.selling[offer] = [quantity, price, item_type, rarity, description]
            # Dictionary will all the different trades to be displayed

    def display(self):
        offer_number = 0
        self.offer_list = []
        for offer in list(self.selling.keys()):
            offer_number += 1
            offer_details = self.selling[offer]
            quantity = offer_details[0]
            price = offer_details[1]
            item_type = offer_details[2]
            rarity = offer_details[3]
            description = offer_details[4]
            print(f"({offer_number}) {offer} - {price} coins each. {quantity} remaining")
            print(f"{rarity.upper()} {item_type}: {description}\n")
            self.offer_list.append(offer)

    def check_single(self, slot_number):
        # slot_number (integer): User input that describes which item they want to buy
        buying_key = self.offer_list[slot_number - 1]
        quantity = self.selling[buying_key][0]
        if quantity == 1:
            return True
        else:
            return False

    def buy(self, slot_number, coins, amount):
        # Transaction
        # slot_number (integer): User input that describes which item they want to buy
        # coins (integer): The amount of money the user has
        # amount (integer): The amount of items the user wants to buy, not the quantity of available stock
        buying_key = self.offer_list[slot_number - 1]
        buying_value = self.selling[buying_key]
        # Shop out of stock
        if amount > buying_value[0] or buying_value[0] == 0:
            print("Transaction failed! Insufficient stock.")
            return buying_key, 0, False
        price = amount * buying_value[1]
        # Checking number of coins
        if coins >= price:
            quantity_left = buying_value[0] - amount
            buying_value[0] = quantity_left
            self.selling[buying_key] = buying_value
            print("Transaction success!")
            print(f"Bought {buying_key} x{amount} for {price} coins each.")
            return buying_key, price, True
        else:
            print("Transaction failed! Insufficient coins.")
            return buying_key, 0, False
