#!/usr/bin/python2
#
#~~monsters.py~~

from time import sleep
import actions

class create(object):
    def  __init__(self, health, damage_dealt, name):
        self.health = health
        self.damage_dealt = damage_dealt
        self.name = name

    def attack (self, newPlayer):
        #TODO: create monsters with different names/health/damage to keep things interesting
        actions.clearscreen()
        print "\nYou were attacked by a %s!" % self.name
        newPlayer.take_damage(self.damage_dealt)
        choice = raw_input("\nDo you F)ight it or R)un away? ")
        choice = choice.lower()
        if choice == "f":
            #TODO: create turn-based fighting class
            print "\nYou decided to fight it. Bad idea! You took 15 damage."
            newPlayer.take_damage(self.damage_dealt)
            return newPlayer
        else:
            print "\nYou decided to run away like a scared child!"
            sleep(2)
            return newPlayer
