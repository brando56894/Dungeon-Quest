#!/usr/bin/python2
#
#~~monsters.py~~

from time import sleep
from random import randint
import actions

class create(object):
    def  __init__(self, health, damage_dealt, name):
        self.health = health
        self.damage_dealt = damage_dealt
        self.name = name
        
    def __str__(self):
        return self.name

    def attack (self, newPlayer):
        #TODO: create monsters with different names/health/damage to keep things interesting
        actions.clearscreen()
        print "\nYou were attacked by a %s!" % self.name
        newPlayer.take_damage(self.damage_dealt)
        choice = raw_input("\nDo you F)ight it or R)un away? ")
        choice = choice.lower()
        if choice == "f":
            print "\nYou decided to fight it. Bad idea!"
            while self.health > 0: 
                print "\n***********************************************************"
                newPlayer.deal_damage(self)
                sleep(1)
                
                #monster still attacks after being killed unless health is checked beforehand
                if self.health > 0:
                    self.deal_damage(newPlayer)
                    #print "************************************************************"
                    sleep(1)
            return newPlayer
        else:
            print "\nYou decided to run away like a scared child!"
            sleep(2)
            return newPlayer
    
    def dragon_attack (self, newPlayer):
        actions.clearscreen()
        print "\nYou were attacked by a %s!" % self.name
        newPlayer.take_damage(self.damage_dealt)
        while self.health > 0: 
            newPlayer.deal_damage(self)
            sleep(1)
            
            #monster still attacks after being killed unless health is checked beforehand
            if self.health > 0:
                self.deal_damage(newPlayer)
                sleep(1)
        return newPlayer
    
    def take_damage(self, damage_taken, newPlayer):
        self.health -= damage_taken
        print "\nThe %s took %d damage! Its health is now at %d" % (self.name,damage_taken,self.health)
        if self.health <= 0:
            print "\nYou killed the %s!" % self.name
            newPlayer.gain_xp(self.name)
        sleep(2)
        return self
    
    def deal_damage(self, newPlayer):
        print "\nThe %s attacked and dealt %d damage!" % (self.name, self.damage_dealt)
        newPlayer.take_damage(self.damage_dealt)
        return newPlayer
