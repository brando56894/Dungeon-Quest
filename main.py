#!/usr/bin/python2
#
#~main.py~

import actions
import player
from time import sleep

version = 1.11 

#enables the debug menu option in the main menu
DEBUG_MODE = "enabled"
#DEBUG_MODE = "disabled"

if DEBUG_MODE == "enabled":
    import debug

def menu(Player):
    actions.clearscreen()
    print "Current Health: %d" % Player.health
    print "\nWhat would you like to do?\n"
    print "***********************"
    print "** 1: Roll Dice      **"
    print "** 2: List Inventory **"
    print "** 3: Change Weapon  **"
    print "** 4: Visit Shop     **"
    print "** 5: Use Potion     **"
    print "** 6: Save Game      **"
    print "** 7: Load Game      **"
    print "** 8: Quit           **"
    if DEBUG_MODE == "enabled":
        print "** 0: Debug Menu     **"
    print "***********************"
    
    choice = raw_input("\nChoice: ") 
    
    if choice == '1':
        actions.roll_dice(Player)
    
    elif choice == '2':
        newPlayer.list_inventory()
    
    elif choice == '3':
        newPlayer.set_current_weapon()
    
    elif choice == '4':
        actions.visit_shop(Player)
    
    elif choice == '5':
        newPlayer.use_potion()
        
    elif choice == '6':
        actions.save_game(newPlayer)
        
    elif choice == '7':
        print "doesn't work yet..."
        sleep(2)
        #actions.load_game
    
    elif choice == '8':
        actions.quit_game()
        
    elif choice == '0':
        debug.menu(Player)
    
    else:
        print ("\nYou didn't select a valid choice.")
        print ("Please choose again.")
        sleep(2)

#Starts the game
actions.clearscreen()
print "Dungeon Quest v%.2f" % version
#name = raw_input("\nWho dares to enter the dungeon? ")
name = "Bran"
newPlayer = player.CreatePlayer(name)

while newPlayer.health > 0:
    menu(newPlayer)
    if newPlayer.basilisk_attack is True:
        print "\nCongratulations! You made it through the dungeon alive!\n"
        exit(0)
    elif newPlayer.run_away > 5:
        clearscreen()
        print "\nYou're too much of a wimp to make it though the dungeon alive!"
        print "Don't show your face here again until you toughen yourself up!\n"
        exit(0)
else:
    print "\nYou were slain! Maybe you should carry more health potions with you next time!\n"
