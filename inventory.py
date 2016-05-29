#!/usr/bin/python2
#
#~inventory.py~

from time import sleep
import misc

def initialize():
    global weapons
    global inv
    
    weapons = {'dagger': 5}
    """
    inventory index
    0 health
    1 health potions
    2 gold
    3 xp
    """
    inv = [100,0,0,0]
    
def list_inventory():
    global inv
    print "\nYou currently have %d health potions, and %d pieces of gold" % (inv[1],inv[2])
    sleep(2)
