#!/usr/bin/python2
#
#~~Player Functions~~

import random
from time import sleep
import actions
import weapons

class create(object):
  
    def __init__(self, name):
        self.health = 100
        self.xp = 0
        self.potions = 0
        self.gold = 0
        self.weapons = []
        self.name = name
        self.steps = 0
        self.current_weapon = "dagger"
        self.add_weapon("dagger",5)
        self.dragon_attack = False
        
    def __repr__(self):
        return self.name

    def find_gold(self):
        amount = random.randint(1,20)
        self.gold += amount
        print "\nYou found %d gold coins, which brings you to a total of %d coins!" % (amount, self.gold)
        sleep(2)
        return self
    
    def find_gold_debug(self,amount):
        self.gold += amount
        print "\nYou found %d gold coins, which brings you to a total of %d coins!" % (amount, self.gold)
        sleep(2)
        return self
    
    def find_potions(self):
        print "\nYou found a health potion!"
        self.potions += 1
        print "You currently have %d potions in your backpack." % self.potions
        sleep(2)
        return self
    
    def buy_potions(self):
        print "Each potion costs 20 gold pieces and restores 25 HP."
        amount = raw_input("\nHow many would you like to purchase? ")
        cost = int(amount) * 20
        if self.gold >= int(cost):
            self.gold = self.gold - int(cost)
            self.potions += int(amount)
            print "\n%d potions have been added to your inventory." % int(amount)
            sleep(2)
            return self
        else:
            print "\nSorry you don't have enough gold for %d potions!" % int(amount)
            sleep(2)
            actions.visit_shop(self)
    
    def use_potion(self):
        if self.potions > 0:
            self.potions -= 1
            self.health += 25
            print "\nYour health is now at %d" % self.health
        else:
            print "\nSorry you don't have any more potions!"
        sleep(2)
        return self
        
    def list_inventory(self):
        actions.clearscreen()
        print "\nName: "+self.name
        print "Exp. Points: %d" % self.xp
        print "Potions Held: %d" % self.potions
        print "Gold: %d pieces" % self.gold
        print "Weapons: %s" % self.weapons[0:]
        print "Current Weapon: %s" % self.current_weapon
        sleep(4)
        
    def low_health(self):
        print "\n*****DANGER*****\n"
        choice = raw_input("\nYour health is currently at %d, and you currently have %d potions in your inventory. \nWould you like to use one? " % (self.health,self.potions))
        choice.lower()
        if choice == 'y' or choice == 'yes':
            self.use_potion(self)
            return self
        else:
            print "\nOk tough guy."
            sleep(2)
            return self
    
    def set_health(self, newHealth):
        self.health = newHealth
        print "\nHealth set to %d" % self.health
        sleep(2)
        return self
    
    def take_damage(self, damage):
        self.health -= damage
        print "Your health is now at %d" % self.health
        if self.health < 0:
            print "\nYou were slain! Maybe you should carry more health potions with you next time!"
            exit(0)
        sleep(2)
        return self

    def deal_damage(self,monster):
        if self.current_weapon == "dagger":
            monster.take_damage(5, self)
        
        if self.current_weapon == "sword":
            monster.take_damage(25, self)    
        
        if self.current_weapon == "pistol":
            monster.take_damage(60, self)
        
        if self.current_weapon == "rifle":
            monster.take_damage(120, self)
    
    def gain_xp(self,monster_name):
        if monster_name == "Dragon":
            gained = random.randint(40,150)
        elif monster_name == "Small Monster":
            gained = random.randint(1,35)
        elif monster_name == "Big Monster":
            gained = random.randint(15,50)
        else:
            gained = random.randint(1,30)
        self.xp += gained
        print "\nYou gained %d XP!" % gained
        return self

    def find_weapon(self):
        weapons = ["sword","pistol","rifle"]
        found = random.choice(weapons)
        print "\nYou found a %s!" % found
        if found == "sword":
            damage = 25
        elif found == "pistol":
            damage = 60
        else:
            damage = 120
        self.add_weapon(found,damage)
        sleep(2)
        return self 
    
    def add_weapon(self,name,damage):
        newWeapon = weapons.create(name,damage)
        self.weapons.append(newWeapon)
        return self
    
    def buy_weapon(self):
        print "\nS)word:   25 Gold"
        print "P)istol:  60 Gold"
        print "R)ifle:   120 Gold"
        choice = raw_input("\nWhich one would you like to purchase? ")
        choice = choice.lower()
        if choice == 's'and self.gold >= 25:
            self.gold -= 25
            self.add_weapon("sword",25)
            print "\nA sword has been added to your inventory."
            sleep(2)
        elif choice == 'p' and self.gold >= 60:
            self.gold -= 60
            self.add_weapon("pistol",60)
            print "\nA pistol has been added to your inventory."
            sleep(2)
        elif choice == 'r' and self.gold >= 120:
            self.gold -= 120
            self.add_weapon("rifle",120)
            print "\nA rifle has been added to your inventory."
            sleep(2)
        else:
            print "\nSorry you don't have enough gold for that purchase."
            sleep(2)
            actions.visit_shop(self)
        return (self)
    
    def set_current_weapon(self):
        #TODO: add logic to make sure the player has the weapon in their inventory
        print "\nCurrent Weapon: " + self.current_weapon
        choice = raw_input("Use weapon: ")
        choice = choice.lower()
        if choice == "sword":
            self.current_weapon = "sword"
        elif choice == "pistol":
            self.current_weapon = "pistol"
        elif choice == "rifle":
            self.current_weapon = "rifle"
        else:
            self.current_weapon = "dagger"
        print "\nCurrent weapon has been changed to: %s" % self.current_weapon
        sleep(2)
        return self
