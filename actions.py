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
from items import items

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
    amount = super_randint(1,25)
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
            "items": (items,),
            "armour": (equipment.armour, equipment.calc_cost),
            "weapons": (equipment.weapons, equipment.calc_cost),
            "skills": (skills.skills, skills.calc_cost),
            }
    while not check:
        area = raw_input("%s" % menu).lower()
        for string in areas:
            if area and area in (string[0], string):
                check = True
                area = string
                break
            elif not area:
                print "\nThanks for stopping by!"
                main.confirm()
                return
        else:
            print "Invalid choice."
            main.confirm()
            main.clearscreen(player)
    visit_shop_section(area, areas[area], player)

def visit_shop_section(name, area, player):
    '''
    Displays items available in visited section
    '''

    main.clearscreen(player)
    count = 0
    options = []
    name_cost_descrip = {}
    for key, nested_dict in area[0].items():
        for item_name, info in nested_dict.items():
            if not info.get("no_shop", 0):
                count += 1
                cost = (area[1](info) if len(area) > 1
                        else info["cost"])
                descrip = (describe_ability if
                        info.get("ability_descrip", 0)
                        else equipment.Equipment(item_name).describe_self)
                name_cost_descrip[str(count)] = (cost, descrip, info)
                options.append(item_name.capitalize())
    menu = main.create_menu(
            prompt = (name.capitalize(), "What do you want to check out?"),
            choices = tuple([str(x+1) for x in range(count)]),
            options = tuple(options),
            enter_option = True
            )
    print menu
    answer = raw_input("")
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
    try:
        descrip = cost_descrip[1]()
    except TypeError:
        descrip = cost_descrip[1](name, cost_descrip[2])
    print "%s\nCost: %d\n\nPres Enter To Go Back\n" %(descrip, cost)
    if not yes:
        answer = raw_input("Do you want to buy this? ").lower()
        if not answer:
            visit_shop_section(section, section_dict, player)
            return
    if yes or "y" in answer:
        if not yes:
            checkout_item(name, cost_descrip, section,
                    section_dict, player, True)
            return
        if section != "skills":
            try:
                answer = raw_input("How many do you want to buy? ").lower()
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
            visit_shop(player)
        else:
            print "\nYou can't pay for that purchase!"
            main.confirm()
            checkout_item(name, cost_descrip, section,
                    section_dict, player, True)
            return
    elif "n" in answer:
        visit_shop_section(section, section_dict, player)
    else:
        print "\nPlease type either 'yes' or 'no'."
        main.confirm()
        checkout_item(name, cost_descrip, section,
                section_dict, player)

def describe_ability(name, dic):
    '''
    Used to describe skills and items
    '''

    string = "%s\n--------------\n" %(name.capitalize())

    #type
    string += ("Type: %s\n" %(dic["type"]) if "type" in dic
            else "")

    #target
    target = dic.get("target", 0)
    if target:
        string += ("Target: " + ("all allies" if target == 2
            else "all enemies" if target == 3 else "You")
            + '\n')

    #base_atk, base_acc
    string += ("" if not dic.get("base_atk", 0) else
            ("Strength: %d\n" %(dic["base_atk"])))
    string += ("" if not dic.get("base_acc", 0) else
            ("Accuracy: %d\n" %(dic["base_acc"])))

    #sp_used, mp_used
    string += (("SP Used: %d\n" %(dic["sp_used"]))
            if dic.get("sp_used", 0) else
            ("MP Used: %d\n" %(dic["mp_used"])) if
            dic.get("mp_used", 0) else "")

    #ability description
    string += "\n%s\n" %(dic["ability_descrip"])
    return string

def quit_game():
    print "\nGood Bye!\n"
    return 0

#TODO: fix me!
def save_game(player):
    with open("savegame.pkl",'wb') as oput:
        pickle.dump(player,oput,pickle.HIGHEST_PROTOCOL)
    print "\nGame saved!"
    main.confirm()

def load_game(player): 
    #input is a key word in python
    with open('savegame.pkl','rb') as iput:
        player.update(pickle.load(iput))
    print "\nSaved game has been loaded!"
    main.confirm()
