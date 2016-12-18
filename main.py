#!/usr/bin/python2
#
#~main.py~

import actions
import player
from time import sleep
from os import system, name

version = 2.0

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
    '''
    clears the screen and prints the HUD if the player
    object is passed
    '''

    system('cls' if name == 'nt' else 'clear')
    if player: #do not pass the player if you don't want HUD to be displayed
        player.HUD()

def confirm():
    '''
    Pauses game until player presses enter
    '''

    raw_input("\n**Press Enter**")

def create_menu(prompt = '', choices = (), options = (),
        enter_option = False):
    '''
    creates a menu

    prompt is the message that will be displayed at the top

    choices are a tuple of letters/numbers that the user
    will type in to access the options

    options are a tuple of words that represent the thing
    the user can access

    the enter_option is for adding a "press enter to go back"
    signal at the end of the menu
    '''
    longest = lambda x, y: x if (len(x) > len(y)) else y
    choices = [x.capitalize() for x in choices]
    options = [x.capitalize() for x in options]
    if isinstance(prompt, tuple):
        check_prompt = reduce(longest, prompt)
    else:
        check_prompt = prompt
        prompt = (prompt, )
    if enter_option:
        choices.append("Enter")
        options.append("Go back")
    longest_choice = reduce(longest, choices)
    entries = []
    for index, choice in enumerate(choices):
        entry = "%s: " % choice
        buff = " " * (len(longest_choice) - len(choice))
        entry += "%s%s" %(buff, options[index])
        entries.append(entry)
    longest_string = reduce(longest, [check_prompt] + [entries[i]
                            + (" " * 6) for i in range(len(entries))])
                            #" " * 6 is a buffer for entries
    length = len(longest_string)
    longest_entry = reduce(longest, entries)
    menu = ""
    for part in prompt:
        part = part.capitalize()
        menu += ("%s\n" % part.center(length, "-"))
    menu += "%s\n" %("*" * length)
    for index, entry in enumerate(entries):
        buff = " " * (len(longest_entry) - len(entry))
        entry = (entry + buff).center(length - 6)
        string = "** %s **\n" %entry
        menu += string
    menu += (("*" * length) + "\n")
    return menu

def create_info_board(heading = '', body = ''):
    '''
    creates info board

    heading is what goes on top of board

    body is what goes in the middle
    '''

    h_parts = heading.split('\n')
    b_parts = []
    if len(h_parts) > 1:
        for x in h_parts[1]:
            if x != '-':
                break
        else:
            heading = h_parts[0]
            h_parts.remove(h_parts[0])
            h_parts.remove(h_parts[0])
            b_parts = h_parts

    heading = heading.capitalize()
    longest = lambda x, y: x if (len(x) > len(y)) else y
    if not b_parts:
        b_parts = body.split('\n')
    buff_b_parts = [x + (' ' * 6) for x in b_parts]
    longest_string = reduce(longest, buff_b_parts + [heading])
    length = len(longest_string)

    info_board = "%s\n%s\n" %(heading.center(length, '-'),
            ('*' * length))
    for string in b_parts:
        info_board += "** %s **\n" %(string.center(length - 6))
    info_board += ("%s\n" %('*' * length))
    return info_board

def combine(*displays):
    '''
    combines different displays and makes
    them uniform
    '''
    
    longest = lambda x, y: x if (len(x) > len(y)) else y
    samples = [display.split('\n')[0] for display in displays]
    longest_sample = reduce(longest, samples)
    length = len(longest_sample)
    longest_display = display[samples.index(longest_sample)]
    combined_display = ''
    for display in displays:
        if display == longest_display:
            combined_display += display
        else:
            new_display = ''
            for line in display.split('\n'):
                if not line:
                    continue
                elif line[:2] != "**":
                    new_display += line.center(length, '-')
                else:
                    middle = line[2:len(line) - 2]
                    if middle == ("*" * len(middle)):
                        buff = "*"
                    else:
                        buff = " "
                    new_display += ("**%s**" %(middle.center(length-4, buff)))
                new_display += '\n'
            combined_display += new_display
    return combined_display

cache = None #place to remember last function

def main_menu(player):
    global cache, new_player

    clearscreen(player)
    start_screen = create_menu(
            prompt = "What would you like to do?",
            choices = ("Enter", "R", "G", "I", "E", "V", "C",
                "S", "L", "Q"),
            options = ("Prev Action", "Roll Dice", "Go To Shop",
                "Inventory", "Equipment", "View Skills", "Check Stats",
                "Save Game", "Load Game", "Quit"),
            )
    print start_screen
    
    choice = raw_input("\nChoice: ").lower()
    #using this method helps clean up all those logic gates
    choices = {
            'r': actions.roll_dice,
            'g': actions.visit_shop,
            'i': player.view_inv,
            'e': player.view_equip,
            'v': player.view_skills,
            'c': player.view_stats,
            's': actions.save_game,
            'l': actions.load_game,
            'q': actions.quit_game,
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
    return 1

if __name__ == "__main__":
    #Starts the game
    #clearscreen()
    #print "Dungeon Quest v%.2f" % version
    #name = raw_input("\nWho dares to enter the dungeon? ")

    #quick player definition taken from battle.py
    new_player = player.Player(**{"name": "Brandon",
        "equipment": {
            "head": "cap",
            "body": "rusty chainmail",
            "both_hands": "rifle",
            "legs": "leather greaves"
            },
        "skills": ["smokescreen", "trip", "focus shot"],
        "stats": {"gold": 99999999999} #dev buff
        })

    while new_player.stats["hp"] > 0:
        continue_game = main_menu(new_player)
        if new_player.stats["basilisk_attack"]:
            print "\nCongratulations! You made it through the dungeon alive!\n"
            break
        elif new_player.stats["run_away"] > 5:
            clearscreen()
            print ("\nYou're too much of a wimp to make it though the dungeon alive!\n"
                    "Don't show your face here again until you toughen yourself up!\n")
            break
        elif not continue_game:
            break
    if not new_player.stats["hp"]:
        print "\nYou were slain! Maybe you should carry more health potions with you next time!\n"
