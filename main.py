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
    """
    clears the screen and prints the HUD if the
    player object is passed

    :player: the player object, defaults to None
    :returns: void

    """
    system('cls' if name == 'nt' else 'clear')
    if player: #do not pass the player if you don't want HUD to be displayed
        player.HUD()
def flush():
    """
    Flushes the stdin buffer

    Best if used with raw_input after sleep so that
    any key pressed by the user does not interfere with
    the raw_input call

    :returns: void

    """
    try: #Linux support
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    #TODO: Test on windows
    except ImportError: #Windows support
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()

def confirm():
    """
    pauses game until player presses enter

    :returns: void

    """
    flush()
    raw_input("\n**Press Enter**")

def create_menu(prompt, choices, options, enter_option = False):
    """
    creates a menu of choices for the user to select from

    :prompt: a string or a tuple/list of strings that will be
             the header of the menu
    :choices: a tuple/list that the user will choose from
              will appear on left of menu
    :options: a tuple/list that usually describes the choices
              Ex: if choice is 'G' option is 'Go To Shop'
              will appear on right of menu
    :enter_option: adds a enter option to the menu to go back
                   defaults to False
    :returns: menu as string

    """
    #lambda used to find longest string given
    longest = lambda x, y: x if (len(x) > len(y)) else y

    #capitalize choices and options
    choices = [x.capitalize() for x in choices]
    options = [x.capitalize() for x in options]

    #raise error if len(choices) != len(options)
    if len(choices) != len(options):
        raise ValueError("Options list must be the same length "
                "as the choices list")

    #if there are multiple prompts get the longest prompt and
    #save in check_prompt
    if isinstance(prompt, tuple) or isinstance(prompt, list):
        check_prompt = reduce(longest, prompt)
    else:
        check_prompt = prompt
        prompt = (prompt, )

    #add enter option
    if enter_option:
        choices.append("Enter")
        options.append("Go back")

    #define longest choice string and format each choice/option line
    longest_choice = reduce(longest, choices)
    entries = []
    for index, choice in enumerate(choices):
        entry = "%s: " % choice
        buff = " " * (len(longest_choice) - len(choice))
        entry += "%s%s" %(buff, options[index])
        entries.append(entry)

    #define longest string, " " * 6 is a buffer for entries
    #the buffer represents the '**  **' that will surround the line
    longest_string = reduce(longest, [check_prompt] + [entries[i]
                            + (" " * 6) for i in range(len(entries))])

    #get longest entry and save length of longest string
    length = len(longest_string)
    longest_entry = reduce(longest, entries)

    #format each line and add it to menu
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

    #add a closing line of *'s
    menu += (("*" * length) + "\n")

    #return menu as string
    return menu

def create_info_board(heading, body):
    """
    creates info board that displays information
    rather than choices

    :heading: Heading of the board, will be at top of board
    :body: Body text of board, will be in the middle of the board
    :returns: info_board as string

    """
    #define longest lambda used for getting longest given string
    longest = lambda x, y: x if (len(x) > len(y)) else y

    #get longest string in heading if heading is a list or tuple
    if isinstance(heading, tuple) or isinstance(heading, list):
        check_heading = reduce(longest, heading)
    else:
        check_heading = heading
        heading = (heading, )

    #split body into separate lines and get longest string
    b_parts = body.split('\n')
    #buff of ' ' * 6 represents the '**  **' that will surround
    #the lines of the body
    buff_b_parts = [x + (' ' * 6) for x in b_parts]
    longest_string = reduce(longest, buff_b_parts + [check_heading])
    length = len(longest_string)

    #define info_board and add heading
    info_board = ""
    for part in heading:
        part = part.capitalize()
        info_board += "%s\n" % part.center(length, '-')

    #separate heading from body using lines of '*'
    info_board += "%s\n" %('*' * length)

    #add lines of body to info_board
    for string in b_parts:
        info_board += "** %s **\n" %(string.center(length - 6))

    #finish off with line of '*'
    info_board += ("%s\n" %('*' * length))

    #return info_board as string
    return info_board

def combine(*displays):
    """
    combines different displays and makes
    them uniform

    :displays: display strings
    :returns: combined display as string

    """
    #lambda to find longest string
    longest = lambda x, y: x if (len(x) > len(y)) else y

    #only need 1 sample string to measure width of display
    #thus the first strings of every display can be compared
    #to find longest display
    samples = [display.split('\n')[0] for display in displays]
    longest_sample = reduce(longest, samples)
    length = len(longest_sample)
    longest_display = display[samples.index(longest_sample)]

    #Begin creating combined_display
    combined_display = ''
    for display in displays:
        #processing not needed for longest display
        if display == longest_display:
            combined_display += display
        else:
            #recreate display
            new_display = ''
            for line in display.split('\n'):
                #skip lines with just '\n'
                if not line:
                    continue
                #recenter headers/prompts
                elif line[:2] != "**":
                    new_display += line.center(length, '-')
                else:
                    #retrieve middle line
                    middle = line[2:len(line) - 2]
                    #readjust length of lines that are just '*'
                    if middle == ("*" * len(middle)):
                        buff = "*"
                    #rebuff content lines
                    else:
                        buff = " "
                    new_display += ("**%s**" %(middle.center(length-4, buff)))
                new_display += '\n'
            #add new_display to combined_display
            combined_display += new_display
    #return combined_display as string
    return combined_display

cache = None #place to remember last function

def main_menu(player):
    global cache, new_player

    clearscreen(player)

    #create start menu
    start_screen = create_menu(
            prompt = "What would you like to do?",
            choices = ("Enter", "J", "G", "I", "E", "V", "C",
                "S", "L", "Q"),
            options = ("Prev Action", "Continue Journey", "Go To Shop",
                "Inventory", "Equipment", "View Skills", "Check Stats",
                "Save Game", "Load Game", "Quit"),
            )

    flush()
    choice = raw_input("%s\nChoice: " %(start_screen)).lower()
    choices = {
            'j': actions.roll_dice,
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
        #EAFP
        try:
            if choices[choice] != cache:
                cache = choices[choice]
            choices[choice]()
        except TypeError:
            if choices[choice] != cache:
                cache = choices[choice]
            x = choices[choice](player)
            #quit_game should be the only one that returns False/zero
            if x == 0:
                return 0
        except KeyError:
            print ("\nYou didn't select a valid choice.\n"
                    "Please choose again.")
            confirm()
    return 1

if __name__ == "__main__":
    #Starts the game

    #ask for user name
    name = ''
    while not name:
        clearscreen()
        print "Dungeon Quest v%.2f" % version
        name = raw_input("\nWho dares to enter the dungeon? ")

    #dev pre-defined profile
    if name in ("brandon", "Brandon"):
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
    elif name in ("masayume", "MasaYume", "Masayume"):
        new_player = player.Player(name = "MasaYume",
                equipment = {
                    "head": "cap",
                    "body": "rusty chainmail",
                    "right_hand": "gauntlet",
                    "left_hand": "dagger",
                    "legs": "leather greaves"
                    },
                skills = ["speed punch", "zen punch", "backstab"],
                stats = {"gold": 99999999999} #dev buff
                )
    else:
        new_player = player.Player(name = name)

    #autoload player data, if available
    actions.load_game(new_player, auto = True)

    while new_player.stats["hp"] > 0:
        continue_game = main_menu(new_player)
        if new_player.stats['hp'] and new_player.stats["basilisk_attack"]:
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
