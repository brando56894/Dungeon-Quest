#!/usr/bin/python2
#
#~main.py~

import misc
import inventory
import actions
from time import sleep

#enables the debug menu option in the main menu
global DEBUG_MODE
DEBUG_MODE = "enabled"
#DEBUG_MODE = "disabled"

if DEBUG_MODE == "enabled":
    import debug

def menu():
    misc.clearscreen()
    global inv
    print "Current Health: %d" % inventory.backpack["health"]
    print "\nWhat would you like to do?\n"
    print "***********************"
    print "** R: Roll Dice      **"
    print "** L: List Inventory **"
    print "** V: Visit Shop     **"
    print "** Q: Quit           **"
    if DEBUG_MODE == "enabled":
        print "** D: Debug Menu     **"
    print "***********************"
    
    choice = raw_input("\nChoice: ") 
    choice = choice.lower()
    
    if choice == 'r':
        actions.roll_dice()
    
    elif choice == 'l':
        inventory.list_inventory()
    
    elif choice == 'v':
        actions.visit_shop()
    
    elif choice == 'q':
        actions.quit_game()
        
    elif choice == 'd':
        debug.menu()
    
    else:
        print ("\nYou didn't select a valid choice.")
        print ("Please choose again.")
        sleep(1)

#TODO: export stats to file, on launch if file 
#exists skip inventory.initialize() and load 
#stats from file instead

#Sets potions, gold and xp to 0, health to 100
#Equips a dagger that deals 5 damage
inventory.initialize()

#Starts the game
print "Welcome to Dungeon Quest!"
while True:
    menu()
