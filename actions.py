#!/bin/python2
#
#~actions.py~

from time import sleep
from superRandom import *
import anpc
import dill
import pickle
import main
import equipment
import skills
import items

def roll_dice(player):
    #TODO: add more rolls since some options come up too often
    #If zork-style gameplay is enabled, this will no longer be a problem

    roll = super_randrange(1,6)
    player.stats["steps"] += roll

    #mid-game boss
    if player.stats["steps"] >= 100:
        anpc.monster_appearance(player, True)
        player.stats["dragon_attack"] = 1
        return

    #final boss
    elif player.stats["steps"] >= 150:
        anpc.monster_appearance(player, True)
        player.stats["basilisk_attack"] = True
        return

    print "\nYou walked %d paces and..." % roll
    sleep(1)

    main.clearscreen(player)
    if roll == 1:
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
        main.confirm()

    else:
        print ("\nYou're safe for the moment!\n"
                "\nTake a minute to catch your breath")
        if player.stats["hp"] <= 60 and player.inventory["potions"] > 0:
            player.low_health()
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
    menu = main.create_menu(
            prompt = ("Shop", "Which section do you want to go to?"),
            choices = ("I", "A", "W", "S"),
            options = ("Items", "Armour", "Weapons", "Skills"),
            enter_option = True
            )
    check = False
    areas = {
            "items": (items.items, None, items.Item),
            "armour": (equipment.armour, equipment.calc_cost,
                equipment.Equipment),
            "weapons": (equipment.weapons, equipment.calc_cost,
                equipment.Equipment),
            "skills": (skills.skills, skills.calc_cost, skills.Skill),
            }
    area_letter = player.validate_input(
            prompt = menu,
            choices = ("i", "a", "w", "s", ""),
            invalid_prompt = "Invalid choice.",
            show_HUD = True
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
        player, yes = False):
    '''
    displays in depth information on chosen item and
    prompts user on whether or not they want to buy the
    item and how much
    '''

    main.clearscreen(player)
    cost = cost_descrip[0]
    descrip = cost_descrip[1](other = "\nCost: %d" %cost)
    menu = main.create_menu(
            prompt = "Do you want to buy this?",
            choices = ('y', 'n'),
            options = ('yes', 'no'),
            enter_option = True
            )
    info_menu = main.combine(descrip, menu)
    if not yes:
        answer = player.validate_input(
                prompt = info_menu,
                choices = ("y", "n", ""),
                invalid_prompt = "\nPlease type either 'y' or 'n'.",
                show_HUD = True
                )
        if not answer or answer == "n":
            visit_shop_section(section, section_dict, player)
            return
    if yes or "y" in answer:
        if not yes:
            checkout_item(name, cost_descrip, section,
                    section_dict, player, True)
            return
        if section != "skills":
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
            except ValueError:
                print "Please input a number."
                main.confirm()
                checkout_item(name, cost_descrip, section,
                        section_dict, player, True)
                return
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
        else:
            print "\nYou can't pay for that purchase!"
            main.confirm()
            checkout_item(name, cost_descrip, section,
                    section_dict, player, True)
            return

def quit_game():
    print "\nGood Bye!\n"
    return 0

def save_game(player):
    with open("savegame.pkl",'wb') as oput:
        pickle.dump(player,oput,pickle.HIGHEST_PROTOCOL)
    print "\nGame saved!"
    main.confirm()

def load_game(player): 
    with open('savegame.pkl','rb') as iput:
        player.update(pickle.load(iput))
    print "\nSaved game has been loaded!"
    main.confirm()
