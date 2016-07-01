#!/usr/bin/python2
#
#~main.py~

import actions
import player
from time import sleep

version = 1.6 #Update each time a new feature is committed!

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
    print "** C: Change Weapon  **"
    print "** V: Visit Shop     **"
    print "** U: Use Potion     **"
    print "** Q: Quit           **"
    if DEBUG_MODE == "enabled":
        print "** D: Debug Menu     **"
    print "***********************"
    
    choice = raw_input("\nChoice: ") 
    choice = choice.lower()
    
    if choice == 'r':
        actions.roll_dice(newPlayer)
    
    elif choice == 'l':
        newPlayer.list_inventory()
    
    elif choice == 'c':
        newPlayer.set_current_weapon()
    
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
actions.clearscreen()
print "Dungeon Quest v%.2f" % version
name = raw_input("\nWho dares to enter the dungeon? ")
name="Brandon"
newPlayer = player.create(name)

while newPlayer.health > 0:
    menu()
else:
    print "\nYou were slain! Maybe you should carry more health potions with you next time!"
