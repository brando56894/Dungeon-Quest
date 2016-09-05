#!/usr/bin/python2
#
#~main.py~

import actions
import player
from time import sleep
from os import system, name

version = 1.12

#enables the debug menu option in the main menu
#DEBUG_MODE = "enabled"
#DEBUG_MODE = "disabled"

#if DEBUG_MODE == "enabled":
#    import debug

#dictionary of player friendly version of stat names
#for printing purposes
player_friendly_stats = {
        "hp": "health",
        "sp": "skill points",
        "mp": "magic points",
        "def": "defense",
        "str": "strength",
        "md": "magic defence",
        "ma": "magic attack",
        "spe": "speed",
        "lck": "luck",
        "acc": "accuracy",
        "eva": "evasion",
        "lvl": "level",
        "exp": "experience",
        "gold": "gold"
        }

def clearscreen(player = None):
    system('cls' if name == 'nt' else 'clear')
    if player:
        player.HUD()

def confirm():
    raw_input("\n**Press any button**")

cache = None #place to remember last function

def menu(player):
    global cache, new_player

    clearscreen(player)
    start_screen = (
            "\nWhat would you like to do?\n"
            "***************************\n"
            "** Enter: Prev Action    **\n"
            "** R:     Roll Dice      **\n"
            "** G:     Go To Shop     **\n"
            "** I:     Inventory      **\n"
            "** E:     Equipment      **\n"
            "** V:     View Skills    **\n"
            "** L:     List Stats     **\n"
            "** S:     Save Game      **\n"
            "** Q:     Quit           **\n"
            )
    #if DEBUG_MODE == "enabled":
    #    print "%s** D:     Debug Menu     **" %(start_screen)
    print start_screen
    print "***************************"
    
    choice = raw_input("\nChoice: ").lower()
    #using this method helps clean up all those logic gates
    choices = {
            'r': actions.roll_dice,
            'g': actions.visit_shop,
            'i': player.view_inv,
            'e': player.view_equip,
            'v': player.view_skills,
            'l': player.view_stats,
            's': actions.save_game,
            'q': actions.quit_game,
            #'d': debug.menu,
            '': cache, #for convenience
            }

    if not choice and not cache:
        print ("\nThere is no previous action.\n"
                "Please choose again.")
        confirm()
    else:
        try:
            if choices[choice] != cache:
                cache = choices[choice]
            x = choices[choice]()
            if x == 0: #quit_game should be the only one that returns zero
                return 0
        except TypeError:
            if choices[choice] != cache:
                cache = choices[choice]
            choices[choice](player)
        except KeyError:
            print ("\nYou didn't select a valid choice.\n"
                    "Please choose again.")
            confirm()

if __name__ == "__main__":
    #Starts the game
    clearscreen()
    print "Dungeon Quest v%.2f" % version
    #name = raw_input("\nWho dares to enter the dungeon? ")
    new_player = player.Player(**{"name": "Brandon",
        "equipment": {
            "head": "cap",
            "body": "rusty chainmail",
            "both_hands": "rifle",
            "legs": "leather greaves"
            },
        "skills": ["smokescreen", "trip", "focus shot"]
        })

    while new_player.stats["hp"] > 0:
        menu(new_player)
        if new_player.stats["basilisk_attack"]:
            print "\nCongratulations! You made it through the dungeon alive!\n"
            break
        elif new_player.stats["run_away"] > 5:
            clearscreen()
            print ("\nYou're too much of a wimp to make it though the dungeon alive!\n"
                    "Don't show your face here again until you toughen yourself up!\n")
            break
    if not new_player.stats["hp"]:
        print "\nYou were slain! Maybe you should carry more health potions with you next time!\n"
