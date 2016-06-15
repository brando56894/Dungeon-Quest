#!/usr/bin/python2
#
#~~Player Functions~~

from random import randint
import actions

class create(object):
  
    def __init__(self, health, xp, potions, gold, weapons, name):
        self.health = health
        self.xp = xp
        self.potions = potions
        self.gold = gold
        self.weapons = weapons
        self.name = name

class actions(create):
        
    def find_gold(self):
        amount = randint(1,20)
        print "You found %d gold coins!" % amount
        self.gold += amount
        return self
    
    def find_potions(self):
        amount = randint(1-3)
        print "You found %d potions!" % amount
        self.potions += amount
        return self
    
    def buy_potions(self):
        print "You have %d pieces of gold." % self.gold
        print "Each potion costs 20 gold pieces and restores 10 HP."
        amount = raw_input("\nHow many potions would you like to purchase? ")
        if self.gold >= (amount*10):
            self.gold = self.gold - (amount*10)
            print "%d potions have been added to your inventory." % self.potions
            return self
        else:
            print "Sorry you don't have enough gold for %d potions!'" % amount
            actions.visit_shop()
    
    def use_potion(self):
        self.potions -= 1
        self.health += 10
        print "Your health is now at %d" % self.health
        return self
    
    def find_weapon(self):
        #TODO add dictionary of weapons and their damages
        #TODO select a random weapon from that list and add it to the player's inventory'
        print "You found a weapon!"
        return self
        
    def list_inventory(self):
        actions.clearscreen()
        print "Name: "+self.name
        print "Exp. Points: %d" % self.xp
        print "Potions Held: %d" % self.potions
        print "Gold: %d pieces" % self.gold
        
    def low_health(self):
       if self.health <= 60 and self.potions > 0:
            print "\n*****DANGER*****\n"
            choice = raw_input("\nYour health is currently at %d, would you like to use a Health Potion? (y or n) " % self.health)
            choice.lower()
            if choice == 'y':
                use_potion(self)
                return self
            else:
                print "\nOk tough guy."
                return self
    
    def set_health(self, newHealth):
        self.health = newHealth
        return self
