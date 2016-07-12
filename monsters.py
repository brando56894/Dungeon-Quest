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
        return "\nName: %s\nDamage Dealt: %d\nHealth: %d" % (self.name,self.damage_dealt,self.health)

    def attack (self, Player, Weapon):
        actions.clearscreen()
        print "\nYou were attacked by a %s!" % self.name
        Player.take_damage(self.damage_dealt)
        choice = raw_input("\nDo you F)ight it or R)un away? ")
        choice = choice.lower()
        if choice == "f":
            actions.clearscreen()
            print "\nYou decided to fight it. Bad idea!"
            #TODO: add a check to make sure the player is using the best weapon in their inventory
            while self.health > 0: 
                print "\n***********************************************************"
                #Weapon = Player.current_weapon
                Weapon.deal_damage(self,Player)  
                sleep(1)
                
                #monster still attacks after being killed unless health is checked beforehand
                if self.health > 0:
                    self.deal_damage(Player)
                    sleep(1)
                
                Player.low_health() #gives the player a chance to use a potion when health is at 60 or below
            return Player
        else:
            actions.clearscreen()
            print "\nYou decided to run away like a scared child!"
            sleep(2)
            Player.run_away += 1
            return Player
    
    def boss_attack (self, Player):
        actions.clearscreen()
        print "\nA %s blocks your path! There looks to be no way around it.\nPrepare to fight!" % self.name
        sleep(2)
        Player.take_damage(self.damage_dealt)
        while self.health > 0: 
            print "\n***********************************************************"
            Player.deal_damage(self)
            sleep(1)
            
            #monster still attacks after being killed unless health is checked beforehand
            if self.health > 0:
                self.deal_damage(Player)
                sleep(1)
            Player.low_health()
        return Player
    
    def take_damage(self, damage_taken, Player):
        self.health -= damage_taken
        print "\nThe %s took %d damage! Its health is now at %d" % (self.name,damage_taken,self.health)
        if self.health <= 0:
            print "\nYou killed the %s!" % self.name
            Player.gain_xp(self.name)
        sleep(2)
        return Player
    
    def deal_damage(self, Player):
        print "\nThe %s attacked and dealt %d damage!" % (self.name, self.damage_dealt)
        Player.take_damage(self.damage_dealt)
        return Player
