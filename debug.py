#!/usr/bin/python2
#~~debug.py~~

"""
This will allow you to call functions
directly in order to test them out
"""

import actions
import misc
import inventory
from time import sleep

def menu():
    misc.clearscreen()
    print "\n####### DEBUG ########################################"
    print "### Attacks:   B)ig S)mall                         ###"
    print "### Find:      W)eapon P)otion G)old               ###"
    print "### Misc:      H)ealth V)isit Shop  C)hange Health ###"
    print "### Actions:   PA)Potion Actions R)oll Dice        ###"
    print "### Inventory: LI)List II)Initialize               ###"
    print "######################################################"
    choice = raw_input("\nChoice: ")
    choice = choice.lower()
    
    if choice == 'b':
        #attack.small()
        print "not implemented"
        
    if choice == 's':
        #attack.big
        print "not implemented"        
    
    if choice == 'w':
        #actions.find_weapon()
        print "not implemented"
        
    if choice == 'p':
        actions.find_potion()
        
    if choice == 'g':
        amount = int(raw_input("How much? "))
        actions.find_gold(amount)
        
    if choice == 'h':
        global inv
        print inventory.inv[0]
        
    if choice == 'ii':
        print "Inventory initialized"
        inventory.initialize()
        
    if choice == 'li':
        inventory.list_inventory()
        
    if choice == 'v':
        actions.visit_shop()
        
    if choice == 'pa':
        print "Which action? "
        
    if choice == 'r':
        actions.roll_dice()
    
    if choice == 'c':
        global inv
        health = raw_input("To what? ")
        inventory.inv[0] = int(health)
        print "Health has been changed to %d" % inventory.inv[0]
        sleep(2)
