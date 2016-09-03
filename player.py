#!/usr/bin/python2
#
#~~Player Functions~~

from superRandom import super_randint, super_choice
import main
from character import Character
from items import Item
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

    def battle_prompt(self, allies = [], enemies = [], enter = False):
        if enter:
            return raw_input("\n**Press any button**")
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
                    attribute = ("inventory", self.skills)
                while 1:
                    self.list_attribute(attribute[0])
                    print "\nPress Enter To Go Back\n"
                    action = raw_input("Choice: ").lower()
                    if action in attribute[1]:
                        if 'i' in action:
                            itemDict = Item(action).effect
                            if not itemDict.get('target', 0):
                                return self.target_prompt(
                                        Item(action).effect,
                                        allies, enemies)
                            else:
                                return Item(action).effect
                        elif self.SPMP_handle(
                                attribute[1][action]):
                            return self.target_prompt(
                                    attribute[1][action],
                                    allies, enemies)
                        else:
                            print ("\nYou don't have enough "
                                    "sp or mp to do that")
                            self.battle_prompt(enter = True)
                    elif not action:
                        return self.battle_prompt(allies, enemies)
                    else:
                        print "\nInvalid choice"
                        self.battle_prompt(enter = True)
            elif 'r' in action:
                return "run"
            else:
                print "\nInvalid choice."
                self.battle_prompt(enter = True)

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
                self.battle_prompt(enter = True)

    def list_attribute(self, attribute):
        main.clearscreen(self)
        if "inv" in attribute:
            print "Inventory\n----------------"
            if not self.inventory:
                print "Y u no hav nuthing!"
            for item, quantity in self.inventory.items():
                print "%s: %d" %(item, quantity)
        elif "sk" in attribute:
            print ("Skills\n----------------\n%s" %(
                    '\n'.join(self.skills)))
        elif "equi" in attribute:
            print "Equipment\n---------------"
            for part, equipment in self.equipment.items():
                print "%s: %s" %(part, equipment.name)

    def use_item(self, item):
        Item(item).use(self)
        self.battle_prompt(enter = True)

    def low_health(self): #*
        if self.health <= 60 and self.potions > 0:
            print "\n*****DANGER*****\n"
            choice = raw_input("\nYour health is currently at %d, a"
                    "nd you currently have %d potions in your inven"
                    "tory. \nWould you like to use one? " % (self.health,self.potions)
                    )
            choice.lower()
            if choice == 'y' or choice == 'yes':
                self.use_potion()
                return self
            else:
                print "\nOk tough guy."
                self.battle_prompt(enter = True)
                return self
