#!/usr/bin/python2
#
#~~Player Functions~~

import random
from time import sleep
import actions
import monsters

class CreatePlayer(object):
  
    def __init__(self, name):
        self.health = 125
        self.xp = 0 #TODO: use gained XP to gain levels
        self.potions = 0
        self.gold = 0
        self.weapons = ["dagger"]
        self.name = name
        self.steps = 0
        self.damage_dealt = 12
        self.current_weapon = "dagger"
        self.dragon_attack = False
        self.basilisk_attack = False
        self.has_sword = False
        self.has_pistol = False
        self.has_rifle = False
        self.run_away = 0
        self.has_key = False
        
    def __repr__(self):
        return "\nName: %s\nHealth: %d\nXP: %d\nPotions: %d\nGold: %d\nWeapons: %s\nSteps: %d\nCurrent Weapon: %s\nDragon Attack: %s\nBasiliskAttack: %s\nHas Sword: %s\nHas Pistol: %s\nHas Rifle: %s\nTimes Run Away: %d\nHas Key: %s" % (self.name,self.health,self.xp,self.potions,self.gold,self.weapons,self.steps,self.current_weapon,self.dragon_attack,self.basilisk_attack,self.has_sword,self.has_pistol,self.has_rifle,self.run_away,self.has_key)

    def find_gold(self):
        amount = random.randint(5,40)
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
        self.potions += 1
        print "\nYou found a health potion! You now have %d potions in your inventory." % self.potions
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
        return self     
    
    def buy_potions(self):
        print "\nGold: %d" % self.gold
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
        if self.potions > 0 and self.potions < 2:
            self.potions -= 1
            self.health += 25
            print "\nYour health is now at %d" % self.health
        elif self.potions > 1:
            print "\nYou currently have %d potions" % self.potions
            amount = int(raw_input("\nHow many? "))
            raise_health = amount * 25
            self.health += raise_health
            self.potions -= amount
            print "\nYour health is now at %d" % self.health
        else:
            print "\nSorry you don't have any more potions!"
        sleep(2)
        return self
        
    def list_inventory(self,Weapon):
        actions.clearscreen()
        print "\nName: "+self.name
        print "Exp. Points: %d" % self.xp
        print "Potions Held: %d" % self.potions
        print "Gold: %d pieces" % self.gold
        print "Current Weapon: %s" % self.current_weapon
        
        if self.has_pistol is True and "pistol" not in self.weapons:
            self.weapons.append("pistol")
        elif self.has_rifle is True and "rifle" not in self.weapons:
            self.weapons.append("rifle")
        elif self.has_sword is True and "sword" not in self.weapons:
            self.weapons.append("sword") 
        print "Weapons: %s" % ", ".join(str(weapon) for weapon in self.weapons)
        sleep(4)
        
    def low_health(self):
        if self.health <= 60 and self.potions > 0:
            print "\n*****DANGER*****\n"
            choice = raw_input("\nYour health is currently at %d, and you currently have %d potions in your inventory. \nWould you like to use one? " % (self.health,self.potions))
            choice.lower()
            if choice == 'y' or choice == 'yes':
                self.use_potion()
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
        print "\nYour health is now at %d" % self.health
        if self.health < 0:
            print "\nYou were slain! Maybe you should carry more health potions with you next time!\n"
            exit(0)
        sleep(2)
        return self
    
    def deal_damage(self,Monster):
        Monster.take_damage(self.damage_dealt,self)
        
    def gain_xp(self,monster_name):
        if monster_name == "Dragon":
            gained = random.randint(40,150)
        elif monster_name == "Gremlin":
            gained = random.randint(1,35)
        elif monster_name == "Demon":
            gained = random.randint(15,50)
        elif monster_name == "Zombie":
            gained = random.randint(16,75)
        else:
            gained = random.randint(1,30)
        self.xp += gained
        print "\nYou gained %d XP!" % gained
        return self

    def add_weapon(self,name,damage):
        if name == "pistol" and self.has_pistol is False:
            self.has_pistol = True            
        elif name == "rifle" and self.has_rifle is False:
            self.has_rifle = True            
        elif name == "sword" and self.has_sword is False:
            self.has_sword = True            
        else:
            print "\nYou already own that weapon!"
        sleep(2)            
        return (self)
    
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
        print "\nCurrent Weapon: " + self.current_weapon
        choice = raw_input("Use weapon: ")
        choice = choice.lower()
        if choice == "sword" and self.has_sword is True:
            self.damage_dealt = 25
            self.current_weapon = "sword"
        elif choice == "pistol" and self.has_pistol is True:
            self.damage_dealt = 60
            self.current_weapon = "pistol"
        elif choice == "rifle" and self.has_rifle is True:
            self.damage_dealt = 120
            self.current_weapon = "rifle"
        elif choice == "dagger":
            self.damage_dealt = 12
            self.current_weapon = "dagger"
        else:
            print "\nSorry you don't currently have that weapon in your inventory."
        print "\nCurrent weapon has been changed to: %s" % self.current_weapon
        sleep(2)
        return self
