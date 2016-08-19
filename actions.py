#!/bin/python2
#
#~actions.py~

from time import sleep
from superRandom import *
import os
import monsters
import pickle

def roll_dice(Player):
    #TODO: add more rolls since some options come up too often
    #If zork-style gameplay is enabled, this will no longer be a problem
    roll = superRandrange(1,6)
    Player.steps += roll
    
    #mid-game boss
    if Player.steps >= 100 and Player.dragon_attack is False:
        dragon = monsters.CreateMonster(150,25,"Dragon") #HP,damage_dealt,name
        dragon.boss_attack(Player)
        Player.dragon_attack = True
        return
    
    #final boss
    elif Player.steps >= 150:
        basilisk = monsters.CreateMonster(300,40,"Basilisk") #HP,damage_dealt,name
        basilisk.boss_attack(Player)
        Player.basilisk_attack = True
        return
    
    print "\nYou walked %d paces and..." % roll
    sleep(1)
    
    clearscreen()
    if roll == 1:
        Player.find_gold()
        
    elif roll == 2:
        print "\nYou stepped on a booby trap!"
        Player.take_damage(superRandint(1,7))
        
    elif roll == 3:
        print "\nYou found a locked door..."
        if Player.has_key is True:
            print "\nYou opened it with the key that you found"
            Player.find_weapon()
        else:
            print "\nBut you can't open it since you don't have the key"
            sleep(2)
        
    elif roll == 4:
        print "\nYou stumbled upon a dead body, you look through it's backpack...."
        sleep(1)
        number = superRandint(0,3)
        if number == 1:
            Player.find_gold()
        elif number == 2:
            Player.find_potions()
        elif number == 3:
            print "\nYou found a key, wonder what it opens..."
            Player.has_key = True
        else:
            print "\nYou didn't find anything...looks like someone else already got to it"
        sleep(2)
        
    elif roll == 5:
        monster_names = ["Gremlin", "Demon", "Zombie"]
        choice = superChoice(monster_names)
        if choice == "Gremlin":
            newMonster = monsters.CreateMonster(superRandint(10,15), superRandint(1,7),"Gremlin") #HP,damage_dealt,name
            newMonster.attack(Player)
            del newMonster
        
        elif choice == "Demon":
            newMonster = monsters.CreateMonster(superRandint(15,25), superRandint(7,15),"Demon") #HP,damage_dealt,name
            newMonster.attack(Player)
            del newMonster
        
        else:
            newMonster = monsters.CreateMonster(superRandint(25,35), superRandint(10,20),"Zombie") #HP,damage_dealt,name
            newMonster.attack(Player)
            del newMonster            
            
    else:
        print ("\nYou're safe for the moment!\n"
                "\nTake a minute to catch your breath")
        if Player.health <= 60 and Player.potions > 0:
            Player.low_health()
        sleep(2)
        
       
def visit_shop(Player):
    clearscreen()
    print ("\nWhat would you like to purchase?\n"
            "You currently have %d gold coins.\n"
            "\nP) Health Potions\n""W) Weapons\n"
            "N) Nothing/Leave Store" %(Player.gold))
    choice = raw_input("\nChoice: ").lower()
    clearscreen()

    if choice == 'p':
        Player.buy_potions()
                    
    elif choice == 'w':
        Player.buy_weapon()
        
    elif choice == 'n':
        print "\nThanks for stopping by!"
        sleep(2)
        return
    
    else:
        print "\nNot a valid choice"
        sleep(2)
        visit_shop(Player)
    
def quit_game():
    print "\nGood Bye!\n"
    exit(0)
    
def save_game(Player):
    with open("savegame.pkl",'wb') as output:
        pickle.dump(Player,output,pickle.HIGHEST_PROTOCOL)
    print "\nGame saved!"
    sleep(1)
    
def load_game(): #TODO: fix me!
    with open('savegame.pkl','rb') as input:
        Player = pickle.load(input)
    print "\nSaved game has been loaded!"
    sleep(2)
    return Player
    
def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')
