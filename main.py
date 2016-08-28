#!/usr/bin/python2
#
#~main.py~

import actions
import player
from time import sleep

version = 1.12 

#enables the debug menu option in the main menu
DEBUG_MODE = "enabled"
#DEBUG_MODE = "disabled"

if DEBUG_MODE == "enabled":
    import debug

cache = None #place to remember last function

def menu(Player):
    global cache

    actions.clearscreen()
    startScreen = ("Current Health: %d\n"
            "\nWhat would you like to do?\n"
            "***************************\n"
            "** Enter: Prev Action    **\n"
            "** R:     Roll Dice      **\n"
            "** L:     List Inventory **\n"
            "** C:     Change Weapon  **\n"
            "** V:     Visit Shop     **\n"
            "** U:     Use Potion     **\n"
            "** S:     Save Game      **\n"
            "** Q:     Quit           **\n" %(Player.health))
    if DEBUG_MODE == "enabled":
        print "%s** D:     Debug Menu     **" %(startScreen)
    print "***************************"
    
    choice = raw_input("\nChoice: ").lower()
    #using this method helps clean up all those logic gates
    choices = {
            'r': actions.roll_dice,
            'l': new_player.list_inventory,
            'c': new_player.set_current_weapon,
            'v': actions.visit_shop,
            'u': new_player.use_potion,
            's': actions.save_game,
            'q': actions.quit_game,
            'd': debug.menu,
            '': cache, #for convenience
            }

    if not choice and not cache:
        print ("\nThere is no previous action.\n"
                "Please choose again.")
        sleep(2)
    else:
        try:
            if choices[choice] != cache:
                cache = choices[choice]
            x = choices[choice]()
            if x == 0:
                return 0
        except TypeError:
            if choices[choice] != cache:
                cache = choices[choice]
            choices[choice](Player)
        except KeyError:
            print ("\nYou didn't select a valid choice.\n"
                    "Please choose again.")
            sleep(2)

#Starts the game
actions.clearscreen()
print "Dungeon Quest v%.2f" % version
#name = raw_input("\nWho dares to enter the dungeon? ")
name = "Bran"
new_player = player.CreatePlayer(name)

while new_player.health > 0:
    if menu(new_player) == 0:
        break
    if new_player.basilisk_attack is True:
        print "\nCongratulations! You made it through the dungeon alive!\n"
        break
    elif new_player.run_away > 5:
        clearscreen()
        print ("\nYou're too much of a wimp to make it though the dungeon alive!\n"
                "Don't show your face here again until you toughen yourself up!\n")
        break
if not new_player.health:
    print "\nYou were slain! Maybe you should carry more health potions with you next time!\n"
