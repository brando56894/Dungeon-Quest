#!/usr/bin/python2
#~~debug.py~~

"""
This will allow you to call functions
directly in order to test them out
"""

import player
import monsters
import actions
from time import sleep

def menu(newPlayer):
    actions.clearscreen()
    print "\n####### DEBUG ########################################"
    print "### Attacks:   M)onster B)oss  F)inal Boss         ###"
    print "### Find:      W)eapon G)old                       ###"
    print "### Misc:      V)isit Shop  C)hange Health         ###"
    print "### Actions:   P)otion Actions R)oll Dice          ###"
    print "### Inventory: L)ist Inventory                     ###"
    print "######################################################"
    choice = raw_input("\nChoice: ")
    choice = choice.lower()
    
    if choice == 'm':
        newMonster = monsters.create(25,15,"Big Monster") #(HP,damage_dealt,name)
        newMonster.attack(newPlayer)
        
    if choice == 'b' or choice == 'f':
        print "not implemented"        
    
    if choice == 'w':
        newPlayer.add_weapon("sword",25)
        
    if choice == 'p':
        newPlayer.find_potions()
        
    if choice == 'g':
        #amount = int(raw_input("How much? "))
        newPlayer.find_gold()
        
    if choice == 'l':
        newPlayer.list_inventory()
        
    if choice == 'v':
        actions.visit_shop()
        
    if choice == 'p':
        print "1) find_potions()"
        print "2) buy_potions()"
        print "3) use_potion()"
        choice = raw_input("Which action?")
        if choice == 1:
            newPlayer.find_potions()
        elif choice == 2:
            newPlayer.buy_potions()
        else:
            newPlayer.use_potion()
       
    if choice == 'r':
        actions.roll_dice()
    
    if choice == 'c':
        health = int(raw_input("To what? "))
        newPlayer.set_health(health)
        sleep(2)
