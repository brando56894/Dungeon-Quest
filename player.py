#!/usr/bin/python2
#
#~~Player Functions~~

from superRandom import super_randint, super_choice
import main
from character import Character
from items import Item, items
from copy import deepcopy

class Player(Character):
  
    def __repr__(self):
        first_part = super(Player, self).__repr__(self)
        second_part = "Steps: %d\nTimes Run Away: %d" %(
                self.stats["steps"], self.stats["run_away"])
        return first_part + second_part

    def build(self, build):
        super(Player, self).build(build)
        for key in ("steps", "run_away", "dragon_attack",
                "basilisk_attack"):
            self.stats[key] = build.get(key, 0)

    def HUD(self):
        string = self.name + '\n'
        for stat in ("hp", "sp", "mp"):
            stat_val = self.stats[stat]
            stat_max = self.stats["max_" + stat]
            string += "%s: %d/%d\n" %(stat, stat_val, stat_max)
        string += ("Level: %d\nGold: %d\n\n" %(
            self.stats["lvl"], self.stats["gold"]))
        print string

    def battle_prompt(self, allies = [], enemies = []):
        while 1:
            main.clearscreen(self)
            string = "What do you want to do?\n-------------------\n"
            for option in ("attack", "skills", "inventory", "run"):
                string += option[:1].upper() + ')' + option[1:] + '\n'
            print string + '\n'
            action = raw_input("Choice: ").lower()
            if 'a' in action:
                return self.target_prompt(self.reg_atk,
                        allies, enemies)
            elif 's' in action or 'i' in action:
                if 's' in action:
                    attribute = ("skills", self.skills)
                else:
                    attribute = ("inventory", self.inventory)
                while 1:
                    print ("%s\nPress Enter To Go Back\n" %(
                        self.list_attribute(attribute[0])))
                    action = raw_input("Choice: ").lower()
                    if action in attribute[1]:
                        if 'i' in action:
                            self.edit_inv(action, 1, True)
                            itemDict = Item(action).effect
                            if not itemDict.get('target', 0):
                                return self.target_prompt(
                                        Item(action).effect,
                                        allies, enemies)
                            else:
                                return itemDict
                        elif self.SPMP_handle(
                                attribute[1][action]):
                            return self.target_prompt(
                                    attribute[1][action],
                                    allies, enemies)
                        else:
                            print ("\nYou don't have enough "
                                    "sp or mp to do that")
                            main.confirm()
                    elif not action:
                        return self.battle_prompt(allies, enemies)
                    else:
                        print "\nInvalid choice"
                        main.confirm()
            elif 'r' in action:
                return "run"
            else:
                print "\nInvalid choice."
                main.confirm()

    def target_prompt(self, atk, allies, enemies):
        while 1:
            main.clearscreen(self)
            display = ""
            if len(allies) - 1:
                display += ("Allies\n------------\n%s\n\n" %(
                        '\n'.join(allies)))
            display += ("Enemies\n------------\n%s\n\n" %(
                '\n'.join(enemies)))
            display += "Press Enter To Go Back\n"
            print display
            target = raw_input("Who is your target? ").lower()
            for char in allies + enemies:
                if target == char.lower():
                    return self.format_atk(deepcopy(atk), char)
            if not target:
                return self.battle_prompt(allies, enemies)
            else:
                print "\nInvalid choice"
                main.confirm()

    def list_attribute(self, attribute, part = ""):
        main.clearscreen(self)
        if "equi" in attribute:
            if "inv" in attribute:
                from equipment import armour, weapons
                string = ("%s\n---------------\n" %(
                    part.replace('_', ' ').capitalize()))
                inv_equip = []
                for item in self.inventory:
                    length = len(inv_equip)
                    for type_name, type_dict in weapons.items():
                        for name in type_dict:
                            if item == name and 'hand' in part:
                                inv_equip.append(item)
                                break
                    if 'hand' in part:
                        part = 'hand'
                    if item in armour[part]:
                        inv_equip.append(item)
                if inv_equip:
                    string += "%s\n" %('\n'.join(inv_equip))
                else:
                    string += "Y u no hav nuthing!!!\n"
                return (string, inv_equip)
            else:
                string = "Equipment\n---------------\n"
                for part, equipment in self.equipment.items():
                    part = part.replace("_", " ").capitalize()
                    string += "%s: %s\n" %(part,
                            (equipment.name if equipment
                                else "None"))
        elif "inv" in attribute:
            string = "Inventory\n----------------\n"
            if not self.inventory:
                string += "Y u no hav nuthing!!!\n"
            for item, quantity in self.inventory.items():
                string += "%s: %d\n" %(item, quantity)
        elif "sk" in attribute:
            string = ("Skills\n----------------\n")
            if not self.skills:
                string += ("You must have mad skillz to not "
                        "have\nany skills and still be alive...\n")
            string += ("%s\n" %('\n'.join(self.skills)))
        elif "sta" in attribute:
            string = "Stats\n----------------\n"
            #dictionaries dont save key order so I have to order them
            for stat in ("hp","sp","mp","def","str","md",
                    "ma","spe","lck","acc","eva","lvl",
                    "exp","gold"):
                value = self.stats[stat]
                if stat in main.player_friendly_stats:
                    string += "%s: %d\n" %(
                            main.player_friendly_stats[
                                stat].capitalize(),
                            value)
        return string

    def view_inv(self, item = None):
        print "%s\nPress Enter To Go Back\n" %(
                self.list_attribute("inventory"))
        answer = raw_input("\nWhat do you want to check out? "
                if self.inventory else "").lower()
        if item or (self.inventory and answer):
            if not item:
                for part, equip in self.equipment.items():
                    if equip and answer == equip.name:
                        item = equip
                        break
                else:
                    item = self.inventory.get(answer, 0)
            if item:
                main.clearscreen(self)
                if isinstance(item, int):
                    from actions import describe_ability
                    for item_type, type_dict in items.items():
                        for name, name_dict in type_dict.items():
                            if name == answer:
                                break
                    print ("%sQuantity: %d\n\nPress Enter "
                            "To Go Back"
                            %(describe_ability(name, name_dict),
                                item))
                    answer = raw_input(
                            "\nWould you like to use this item? "
                            if "any" in item_type else "").lower()
                    if answer:
                        if "y" in answer:
                            self.use_item(name)
                        elif "n" not in answer:
                            print ("Please type either 'yes' "
                                    "or 'no'.")
                            main.confirm()
                            self.view_inv(item)
                else:
                    print ("%s\nPress Enter To Go Back" %(
                        item.describe_self()))
                    raw_input("")
            else:
                print "\nInvalid choice"
                main.confirm()
            self.view_inv()

    def view_equip(self):
        print "%s\nPress Enter To Go Back\n" %(
                self.list_attribute("equipment"))
        answer = raw_input("\nWhat do you want to check out? ").lower()
        if answer:
            for part, equip in self.equipment.items():
                if equip and (
                        answer == part.replace('_', ' ')
                        or answer == equip.name):
                    break
            else:
                print "\nInvalid choice"
                main.confirm()
                self.view_equip()
                return
            main.clearscreen(self)
            print ("%s: %s\nPress Enter To Go Back\n" %(
                part.replace('_',' ').capitalize(),
                equip.describe_self()))
            answer = raw_input("Would you like to equip something "
                    "else here or dequip this item? "
                    if (equip and equip.name != "bare")
                    else "").lower()
            if answer and "d" not in answer:
                string, equip_list = self.list_attribute(
                        "part equipment in inventory", part)
                print "%s\nPress Enter To Go Back\n" %(string)
                answer = raw_input("\nWhat do you want to "
                        "check out? " if equip_list else ""
                        ).lower()
                if answer and answer in equip_list:
                    main.clearscreen(self)
                    from equipment import Equipment
                    equip = Equipment(answer)
                    print ("%s\nPress Enter To Go Back\n" %(
                        equip.describe_self()))
                    answer = raw_input("\nDo you want to equip this? ").lower()
                    if "y" in answer:
                        self.equip(equip, part)
                        print "\n%s was equipped." %(equip.name)
                        main.confirm()
                    elif "n" not in answer:
                        print "\nInvalid choice"
                        main.confirm()
                elif answer:
                    print "\nInvalid choice"
                    main.confirm()
            elif "d" in answer:
                self.equip(equip, part, True)
                print "\n%s was dequipped." %(equip.name)
                main.confirm()
            self.view_equip()

    def view_skills(self):
        print "%s\nPress Enter To Go Back\n" %(
                self.list_attribute("skills"))
        answer = raw_input("\nWhat do you want to check out? "
                if self.skills else "").lower()
        if answer and self.skills:
            if answer in self.skills:
                main.clearscreen()
                atk = self.skills[answer]
                from actions import describe_ability
                raw_input("%s\n\nPress Enter To Go Back"
                        %(describe_ability(answer, atk)))
            else:
                print "\nInvalid choice"
                main.confirm()
            self.view_skills()

    def view_stats(self):
        print self.list_attribute("stats")
        main.confirm()

    def use_item(self, item):
        print ''
        Item(item).use(self)
        self.edit_inv(item, 1, True)
        main.confirm()

    def low_health(self): #*
        health = self.stats["hp"]
        potions = self.inventory["potion"]
        if health <= 60 and potions > 0:
            print "\n*****DANGER*****\n"
            answer = raw_input("\nYour health is currently at %d, a"
                    "nd you currently have %d potions in your inven"
                    "tory. \nWould you like to use one? " % (health, potions)
                    ).lower()
            answer.lower()
            if 'y' in answer:
                self.use_item("potion")
            else:
                print "\nOk tough guy."
                main.confirm()

    def gold_handle(self, cost):
        if self.stats["gold"] < cost:
            return False
        self.stat_modifier({"gold", -cost})
        return True
