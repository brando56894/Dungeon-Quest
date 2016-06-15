#!/usr/bin/python2
#
#~main.py~

import actions
import player
from time import sleep

#enables the debug menu option in the main menu
DEBUG_MODE = "enabled"
#DEBUG_MODE = "disabled"

if DEBUG_MODE == "enabled":
    import debug

def menu():
    actions.clearscreen()
    print "Current Health: %d" % newPlayer.health
    print "\nWhat would you like to do?\n"
    print "***********************"
    print "** R: Roll Dice      **"
    print "** L: List Inventory **"
    print "** V: Visit Shop     **"
    print "** U: Use Potion     **"
    print "** Q: Quit           **"
    if DEBUG_MODE == "enabled":
        print "** D: Debug Menu     **"
    print "***********************"
    
    choice = raw_input("\nChoice: ") 
    choice = choice.lower()
    
    if choice == 'r':
        actions.roll_dice()
    
    elif choice == 'l':
        newPlayer.list_inventory()
    
    elif choice == 'v':
        actions.visit_shop(newPlayer)
    
    elif choice == 'u':
        newPlayer.use_potion()
    
    elif choice == 'q':
        actions.quit_game()
        
    elif choice == 'd':
        debug.menu(newPlayer)
    
    else:
        print ("\nYou didn't select a valid choice.")
        print ("Please choose again.")
        sleep(2)

#Starts the game
print "Dungeon Quest v1.0\n"
#name = raw_input("Who dares to enter the dungeon? ")
name = "Brandon"
#creates a new player with 100 health, 0 xp, 0 potions, 0 gold, and a dagger
newPlayer = player.create(100, 0, 0, 0, "dagger", name)

while True:
    menu()
