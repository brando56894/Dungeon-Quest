#!/usr/bin/python2
#
#~inventory.py~

from time import sleep
import misc

def initialize():
    global inv
    global backpack
    
    """
    inventory index
    0 health
    1 health potions
    2 gold
    3 xp
    """
    inv = [100,0,0,0]
    backpack = {
        "hp": 100,
        "potions": 0,
        "gold": 0,
        "xp": 0,
        "weapons": {'dagger':5}
        }
    
def list_inventory():
    #global inv
    global backpack
    #print "\nYou currently have %d health potions, and %d pieces of gold" % (inv[1],inv[2])
    print "\nYou currently have %d health potions, and %d pieces of gold" % (backpack["potions"],backpack["gold"])
    print "\nYour currently held weapons are:" 
    for weapon in backpack["weapons"]:
        print weapon
    sleep(2)
