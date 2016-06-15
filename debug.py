#!/usr/bin/python2
#~~debug.py~~

"""
This will allow you to call functions
directly in order to test them out
"""

import player
import actions
from time import sleep

def menu(newPlayer):
    actions.clearscreen()
    print "\n####### DEBUG ########################################"
    print "### Attacks:   B)ig S)mall                         ###"
    print "### Find:      W)eapon P)otion G)old               ###"
    print "### Misc:      V)isit Shop  C)hange Health         ###"
    print "### Actions:   PA)Potion Actions R)oll Dice        ###"
    print "### Inventory: LI)List                             ###"
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
        newPlayer.find_weapon()
        
    if choice == 'p':
        player.find_potions()
        
    if choice == 'g':
        amount = int(raw_input("How much? "))
        newPlayer.find_gold(amount)
        
    if choice == 'li':
        newPlayer.list_inventory()
        
    if choice == 'v':
        actions.visit_shop()
        
    if choice == 'pa':
        print "Which action? "
        
    if choice == 'r':
        actions.roll_dice()
    
    if choice == 'c':
        health = raw_input("To what? ")
        newPlayer.set_health(health)
        print "Health has been changed to %d" % newPlayer.health
        sleep(2)
