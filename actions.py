#!/bin/python2
#
#~actions.py~

from time import sleep
from superRandom import *
from random import shuffle
import anpc
import dill
import pickle
import main
import equipment
import skills
import items

def calc_event_probability(luck):
    """TODO: Docstring for calc_event_probability.

    :luck: TODO
    :returns: TODO

    """
    #multiples are from 1 to 100
    gold_chance = int(15 * luck)
    trap_chance = int(10 / luck) #in this case luck decreases probability
    door_chance = int(10 * luck)
    dead_body_chance = int(10 * luck)
    battle_chance = 40
    rest_chance = int(15 * luck)
    event_probability = (
            gold_chance * [1] +
            trap_chance * [2] +
            door_chance * [3] +
            dead_body_chance * [4] +
            battle_chance * [5] +
            rest_chance * [6]
            )
    shuffle(event_probability)
    return event_probability

def roll_dice(player):
    #TODO: add more rolls since some options come up too often
    #If zork-style gameplay is enabled, this will no longer be a problem

    roll = super_choice( calc_event_probability(
        player.check_if_lucky() ) )
    player.stats["steps"] += roll

    print "\nYou walked %d paces and..." % roll
    sleep(1)
    main.clearscreen(player)

    #mid-game boss
    if player.stats["steps"] >= 100 and not player.stats['dragon_attack']:
        anpc.monster_appearance(player, True)
        player.stats["dragon_attack"] = 1
        return

    #final boss
    elif player.stats["steps"] >= 150:
        anpc.monster_appearance(player, True)
        player.stats["basilisk_attack"] = True
        return

    elif roll == 1:
        find_gold(player)

    elif roll == 2:
        damage = super_randint(1, 7)
        player.stat_modifier({"hp": -damage})
        print "\nYou stepped on a booby trap and took %d damage!" % damage
        main.confirm()

    elif roll == 3:
        print "\nYou found a locked door..."
        if "key" in player.inventory:
            print "\nYou opened it with the key that you found"
            find_weapon(player)
            player.edit_inv("key", 1, True)
        else:
            print "\nBut you can't open it since you don't have the key"
            main.confirm()

    elif roll == 4:
        print "\nYou stumbled upon a dead body, you look through it's backpack...."
        sleep(1)
        number = super_randint(1,3)
        if number == 1:
            find_gold(player)
        elif number == 2:
            find_potions(player)
        elif number == 3:
            print "\nYou found a key, wonder what it opens..."
            player.edit_inv("key", 1)
            main.confirm()
        else:
            print "\nYou didn't find anything...looks like someone else already got to it"
            main.confirm()

    elif roll == 5:
        anpc.monster_appearance(player)

    else:
        print ("\nYou're safe for the moment!\n"
                "\nTake a minute to catch your breath")
        if (player.stats["hp"] <= 60) and ("potion" in player.inventory):
            sleep(1)
            player.low_health()
        else:
            main.confirm()

def find_gold(player):
    amount = super_randint(1,25) * player.check_if_lucky()
    player.stat_modifier({"gold": amount})
    print ("\nYou found %d gold coins, which brings "
            "you to a total of %d coins!" % (
                amount, player.stats["gold"]))
    main.confirm()

def find_weapon(player):
    '''
    Creates weapon list and removes weapons not available
    to player
    Then randomly returns a weapon from list
    '''

    weapon_list = []
    for weapon_type in equipment.weapons:
        weapon_list += equipment.weapons[weapon_type].keys()
    cannot_see = ('bare', 'claws') #list of weapons that cannot be bought
    for weapon in cannot_see:
        weapon_list.remove(weapon)
    found = super_choice(weapon_list)
    print "\nYou found a %s!" % found
    player.edit_inv(found, 1)
    main.confirm()

def find_potions(player):
    player.edit_inv("potion", 1)
    print ("\nYou found a health potion! You now have %d "
            "potions in your inventory."
            % player.inventory["potion"])
    main.confirm()

def visit_shop(player):
    '''
    Displays shop sections
    '''

    main.clearscreen(player)
    areas = {
            "items": (items.items, None, items.Item),
            "armour": (equipment.armour, equipment.calc_cost,
                equipment.Equipment),
            "weapons": (equipment.weapons, equipment.calc_cost,
                equipment.Equipment),
            "skills": (skills.skills, skills.calc_cost, skills.Skill),
            }
    area_letter = player.validate_input(
            prompt = ("Shop", "Which section do you want to go to?"),
            choices = ("i", "a", "w", "s"),
            options = ("Items", "Armour", "Weapons", "Skills"),
            show_HUD = True,
            make_menu = True
            )
    for area in areas:
        if area_letter == area[0]:
            break
    else:
        print "\nThanks for stopping by!"
        main.confirm()
        return
    visit_shop_section(area, areas[area], player)

def visit_shop_section(name, area, player): #here
    '''
    Displays items available in visited section
    '''

    main.clearscreen(player)
    count = 0
    options = []
    name_cost_descrip = {}
    for key, nested_dict in area[0].items():
        for item_name, info in nested_dict.items():
            if (not info.get("no_shop", 0) and
                    not ((name == "skills") and
                        (item_name in player.skill_bag or
                            item_name in player.skills))):
                count += 1
                cost = (area[1](info) if area[1]
                        else info["cost"])
                descrip = area[2](item_name).describe_self
                name_cost_descrip[str(count)] = (cost, descrip, info)
                options.append(item_name.capitalize())
    menu = main.create_menu(
            prompt = (name.capitalize(), "What do you want to check out?"),
            choices = tuple([str(x+1) for x in range(count)]),
            options = tuple(options),
            enter_option = True
            )
    answer = raw_input(menu)
    if not answer:
        visit_shop(player)
        return
    try: #EAFP Easier to Ask for Forgiveness than Permission
        cost_descrip_info = name_cost_descrip[answer]
        checkout_item(options[int(answer) - 1].lower(),
                cost_descrip_info, name, area, player)
    except KeyError:
        print "Invalid choice."
        main.confirm()
        visit_shop_section(name, area, player)

def checkout_item(name, cost_descrip, section, section_dict,
        player):
    '''
    displays in depth information on chosen item and
    prompts user on whether or not they want to buy the
    item and how much
    '''

    main.clearscreen(player)
    cost = cost_descrip[0]
    descrip = cost_descrip[1](other = "\nCost: %d" %cost)
    answer = player.validate_input(
            prompt = "Do you want to buy this?",
            combine = descrip,
            YN_menu = True,
            show_HUD = True,
            )
    if not answer or answer == "n":
        visit_shop_section(section, section_dict, player)
        return
    if "y" in answer:
        while 1:
            if section != "skills":
                while 1:
                    main.clearscreen(player)
                    sub_menu = main.create_menu(
                            prompt = "How many do you want to buy?",
                            enter_option = True
                            )
                    sub_info_menu = main.combine(descrip, sub_menu)
                    try:
                        answer = raw_input(sub_info_menu).lower()
                        if not answer:
                            visit_shop_section(section, section_dict, player)
                            return
                        amount = int(answer)
                        break
                    except ValueError:
                        print "Please input a number."
                        main.confirm()
            else:
                amount = 1
            if amount and player.gold_handle(cost * amount):
                print ("\nThank you for your purchase\n"
                        "You bought %d %s" %(amount,
                            (name + 's' if amount > 1 else name)))
                if section == "skills":
                    player.add_skill(name)
                else:
                    player.edit_inv(name, amount)
                main.confirm()
                visit_shop_section(section, section_dict, player)
                break
            else:
                print "\nYou can't pay for that purchase!"
                main.confirm()

def save_game(player, quick = False):
    from os.path import isfile
    #Check if save data exists
    if not quick and isfile('data/%s.pkl' % player.name.lower()):
        if change_since_save(player):
            main.clearscreen()
            answer = player.validate_input(
                    prompt = ("Doing this will overwrite previously saved data.",
                        "Are you ok with this?"),
                    YN_menu = True,
                    enter_option = False
                    )
            if answer != 'y':
                print "\nGame NOT saved!"
                main.confirm()
                return
        else:
            print "No changes to save!"
            main.confirm()
            return
    with open("data/%s.pkl" % player.name.lower(),'wb') as oput:
        pickle.dump(player,oput,pickle.HIGHEST_PROTOCOL)
    print "\nGame saved!"
    main.confirm()

def change_since_save(player):
    """TODO: Docstring for change_since_save.

    :player: TODO
    :returns: TODO

    """
    with open('data/%s.pkl' % player.name.lower(),'rb') as iput:
        return not (player == pickle.load(iput))

def load_save_files(player):
    """TODO: Docstring for load_save_file.

    :player: TODO
    :returns: TODO

    """
    from os import listdir
    data_dir = listdir('data')
    options = []
    for filename in data_dir:
        filename = filename.split('.')
        if filename[1] == 'pkl':
            options.append(filename[0])
    try:
        return options[int(player.validate_input(
                prompt = "Which save file do you want to load?",
                options = options,
                choices = [str(x+1) for x in range(len(options))]
                )) - 1]
    except ValueError:
        return ''

def load_game(player, auto = False):
    from os.path import isfile
    if not auto:
        #get filenames from data folder
        name = load_save_files(player).lower()
        if not name:
            return
    else:
        name = player.name.lower()
    #Check if save data exists
    if isfile('data/%s.pkl' % name):
        with open('data/%s.pkl' % name,'rb') as iput:
            load_player = pickle.load(iput)
            if not auto:
                skip_check = False
                #check for differences between load player and current player
                #if chosen filename equals current player name
                if name == player.name:
                    if player == load_player:
                        print "\nData is already loaded and has not changed!"
                        main.confirm()
                        return
                    else:
                        skip_check = True
                #check if anything changed since last save
                if skip_check or change_since_save(player):
                    answer = player.validate_input(
                            prompt = (
                                "This will overwrite all changes since last save.",
                                "Is this ok?"),
                            YN_menu = True,
                            enter_option = False
                            )
                    if answer != 'y':
                        print '\nLoad aborted!'
                        main.confirm()
                        return
            player.update(load_player)
        if not auto:
            print "\nLoad successful!"
            main.confirm()
            return
    elif not auto:
        print "\nNo saved game data to load!"
        main.confirm()

def quit_game(player):
    #check if game has changed since last save
    if change_since_save(player):
        #ask if they would like to save first
        answer = player.validate_input(
                prompt = "Do you want to save before you quit?",
                YN_menu = True
                )
        if answer == 'y':
            save_game(player, True)
        elif not answer:
            return 1 #go back
    print "\nGood Bye!\n"
    return 0
