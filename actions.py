#!/bin/python2
#
#~actions.py~

from time import sleep
from superRandom import *
import os
from anpc import *
import pickle
from equipment import weapons, calc_cost

def roll_dice(player):
    #TODO: add more rolls since some options come up too often
    #If zork-style gameplay is enabled, this will no longer be a problem

    roll = super_randrange(1,6)
    player.stats["steps"] += roll

    #mid-game boss
    if player.stats["steps"] >= 100:
        monster_appearance(player, True)
        player.stats["dragon_attack"] = 1
        return

    #final boss
    elif player.stats["steps"] >= 150:
        monster_appearance(player, True)
        player.stats["basilisk_attack"] = True
        return

    print "\nYou walked %d paces and..." % roll
    sleep(1)

    clearscreen()
    if roll == 1:
        find_gold(player)

    elif roll == 2:
        print "\nYou stepped on a booby trap!"
        player.statModification({"hp": -super_randint(1,7)})

    elif roll == 3:
        print "\nYou found a locked door..."
        if "key" in player.inventory:
            print "\nYou opened it with the key that you found"
            find_weapon(player)
            player.edit_inv("key", 1, True)
        else:
            print "\nBut you can't open it since you don't have the key"
            sleep(2)

    elif roll == 4:
        print "\nYou stumbled upon a dead body, you look through it's backpack...."
        sleep(1)
        number = super_randint(0,3)
        if number == 1:
            find_gold(player)
        elif number == 2:
            find_potions(player)
        elif number == 3:
            print "\nYou found a key, wonder what it opens..."
            player.edit_inv("key", 1)
            sleep(2)
        else:
            print "\nYou didn't find anything...looks like someone else already got to it"
            sleep(2)

    #all of #5 I will do later
    elif roll == 5:
        monster_appearance(player)

    else:
        print ("\nYou're safe for the moment!\n"
                "\nTake a minute to catch your breath")
        if player.health <= 60 and player.inventory["potions"] > 0:
            player.low_health()
        sleep(2)

def find_gold(player):
    amount = super_randint(1,25)
    player.statModification({"gol": amount})
    print ("\nYou found %d gold coins, which brings "
            "you to a total of %d coins!" % (
                amount, player.stats["gold"]))
    sleep(2)

#untouched, just moved
def find_gold_debug(self,amount):
    self.gold += amount
    print "\nYou found %d gold coins, which brings you to a total of %d coins!" % (amount, self.gold)
    sleep(2)
    return self

def find_weapon(player):
    weapon_list = []
    for weapon_type in weapons:
        weapon_list += weapon_type.keys()
    found = super_choice(weapon_list)
    print "\nYou found a %s!" % found
    player.edit_inv(found, 1)

def find_potions(player):
    player.edit_inv("potion", 1)
    print ("\nYou found a health potion! You now have %d "
            "potions in your inventory."
            % player.inventory["potions"])
    sleep(2)

def visit_shop(player):
    clearscreen()
    print ("\nWhat would you like to purchase?\n"
            "You currently have %d gold coins.\n"
            "\nP) Health Potions\n""W) Weapons\n"
            "N) Nothing/Leave Store" %(player.stats["gol"]))
    choice = raw_input("\nChoice: ").lower()
    clearscreen()

    if choice == 'p':
        buy_potions(player)

    elif choice == 'w':
        buy_weapon(player)

    elif choice == 'n':
        print "\nThanks for stopping by!"
        sleep(2)

    else:
        print "\nNot a valid choice"
        sleep(2)
        visit_shop(player)

def buy_potions(player):
    print ("\nGold: %d"
            "Each potion costs 20 gold pieces "
            "and restores 25 HP." % player.stats["gol"])
    while 1:
        try:
            amount = int(raw_input("\nHow many would you like to purchase? "))
            break
        except ValueError:
            print "Please enter a number!"
    cost = amount * 20
    if player.stats["gol"] >= cost:
        player.statModification({"gol": -cost})
        player.edit_inv("potion", amount)
        print "\n%d potions have been added to your inventory." % amount
        sleep(2)
    else:
        print "\nSorry you don't have enough gold for %d potions!" % amount
        sleep(2)
        visit_shop(player)

def buy_weapon(player):
    weapon_costs = {}
    for weapon_type in weapons:
        for weapon, weapon_dic in weapon_type.items():
            if weapon not in ("bare"):
                weapon_costs[weapon] = calc_cost(weapon_dic["mods"])
                print "\n%s: %d Gold" %(weapon.title(),
                        weapon_costs[weapon])
    answer = raw_input("\nWhich one would you like to purchase? ").lower()
    if (answer in weapon_costs and player.stats["gol"]
            >= weapon_costs[answer]):
        player.statModification("gol", -weapon_costs[answer])
        player.edit_inv(answer, 1)
        print "\nA %s has been added to your inventory." % answer
        sleep(2)
    elif answer not in weapon_costs:
        print "\nNot a valid choice."
        sleep(2)
        buy_weapon(player)
    else:
        print "\nSorry you don't have enough gold for that purchase."
        sleep(2)
        visit_shop(player)

def quit_game():
    print "\nGood Bye!\n"
    return 0

def save_game(player):
    with open("savegame.pkl",'wb') as oput:
        pickle.dump(player,oput,pickle.HIGHEST_PROTOCOL)
    print "\nGame saved!"
    sleep(1)

def load_game(): #TODO: fix me!
    #input is a key word in python
    with open('savegame.pkl','rb') as iput:
        player = pickle.load(iput)
    print "\nSaved game has been loaded!"
    sleep(2)
    return player

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')
