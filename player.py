#!/usr/bin/python2
#
#~~Player Functions~~

from random import randint
import actions
from time import sleep

class create(object):
  
    def __init__(self, health, xp, potions, gold, weapons, name):
        self.health = health
        self.xp = xp
        self.potions = potions
        self.gold = gold
        self.weapons = weapons
        self.name = name

    def find_gold(self):
        amount = randint(1,20)
        print "\nYou found %d gold coins, which brings you to a total of %d coins!" % (amount, self.gold)
        self.gold += amount
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
        #PreREQ: finish find_weapon()
        pass
    
    def gain_xp(self):
        #TODO gain XP when player kills a monster and implement leveling system
        #PreREQ finish the fighting system
        pass
