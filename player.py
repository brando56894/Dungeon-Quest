#!/usr/bin/python2
#
#~~Player Functions~~

from random import randint
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
        
        self.add_weapon("dagger",5)
        
    def __repr__(self):
        return self.name

    def find_gold(self):
        amount = randint(1,20)
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
        print "Each potion costs 20 gold pieces and restores 10 HP."
        amount = raw_input("\nHow many would you like to purchase? ")
        if self.gold >= (amount*10):
            self.gold = self.gold - (amount*10)
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
            self.health += 10
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
        print "Weapons: %s" % self.weapons
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
        sleep(2)
        return self

    def deal_damage(self):
        #TODO write class based off of damage of currently wielded weapon
        #PreREQ: finish add_weapon()
        pass
    
    def gain_xp(self):
        #TODO gain XP when player kills a monster and implement leveling system
        #PreREQ finish the fighting system
        pass

    def find_weapon(self):
        #TODO select a random weapon from that list and add it to the player's inventory'
        print "\nYou found a weapon!"
        sleep(2)
        return self 
    
    def add_weapon(self,name,damage):
        newWeapon = weapons.create(name,damage)
        self.weapons.append(newWeapon)
        return self
    
    def buy_weapon(self,player):
        print "\nS)word: 25 Gold"
        print "P)istol:  60 Gold"
        print "R)ifle:   120 Gold"
        choice = raw_input("Which one would you like to purchase? ")
        choice = choice.lower()
        if choice == 's':
            self.gold -= 25
        elif choice == 'p':
            self.gold -= 60
        else:
            self.gold -= 120
        return (self,player)
