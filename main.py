#!/usr/bin/python2
#
#~main.py~

import actions
import player
from time import sleep

version = 1.10 #Update each time a new feature is committed!

#enables the debug menu option in the main menu
DEBUG_MODE = "enabled"
#DEBUG_MODE = "disabled"

if DEBUG_MODE == "enabled":
    import debug

cache = None

def menu(Player):
    global cache

    choices = {
            'r': actions.roll_dice,
            'l': newPlayer.list_inventory,
            'c': newPlayer.set_current_weapon,
            'v': actions.visit_shop,
            'u': newPlayer.use_potion,
            's': actions.save_game,
            'q': actions.quit_game,
            'd': debug.menu,
            '': cache,
            }

    actions.clearscreen()
    print "Current Health: %d" % Player.health
    print "\nWhat would you like to do?\n"
    print "***********************"
    print "** Enter: Prev Action**"
    print "** R: Roll Dice      **"
    print "** L: List Inventory **"
    print "** C: Change Weapon  **"
    print "** V: Visit Shop     **"
    print "** U: Use Potion     **"
    #print "** S: Save Game      **"
    print "** Q: Quit           **"
    if DEBUG_MODE == "enabled":
        print "** D: Debug Menu     **"
    print "***********************"
    
    choice = raw_input("\nChoice: ").lower()

    if not choice and not cache:
        print "\nThere is no previous action."
        print "Please choose again."
        sleep(2)
    else:
        try:
            if choices[choice] != cache:
                cache = choices[choice]
            choices[choice]()
        except TypeError:
            if choices[choice] != cache:
                cache = choices[choice]
            choices[choice](Player)
        except KeyError:
            print ("\nYou didn't select a valid choice.")
            print ("Please choose again.")
            sleep(2)
   # 
   # if choice == 'r':
   #     actions.roll_dice(Player)
   # 
   # elif choice == 'l':
   #     newPlayer.list_inventory()
   # 
   # elif choice == 'c':
   #     newPlayer.set_current_weapon()
   # 
   # elif choice == 'v':
   #     actions.visit_shop(Player)
   # 
   # elif choice == 'u':
   #     newPlayer.use_potion()
   #     
   # elif choice == 's':
   #     actions.save_game()
   # 
   # elif choice == 'q':
   #     actions.quit_game()
   #     
   # elif choice == 'd':
   #     debug.menu(Player)
   # 
   # elif choice == '':
   #     pass
   # else:
   #     print ("\nYou didn't select a valid choice.")
   #     print ("Please choose again.")
   #     sleep(2)

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
