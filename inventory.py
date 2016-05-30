#!/usr/bin/python2
#
#~inventory.py~

from time import sleep
import misc

def initialize():
    global backpack
    
    backpack = {
        "health": 100,
        "potions": 0,
        "gold": 0,
        "xp": 0,
        "weapons": {'dagger':5}
        }
    
def list_inventory():
    global backpack
    
    print "\nYou currently have %d health potions, and %d pieces of gold" % (backpack["potions"],backpack["gold"])
    print "\nYour currently held weapons are:" 
    
    for weapon in backpack["weapons"]:
        print weapon
    sleep(2)
