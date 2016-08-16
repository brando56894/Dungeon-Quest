#!/bin/python2
#
#~actions.py~

from time import sleep
import random
import os
import monsters
import pickle

def roll_dice(Player):
    #TODO: add more rolls since some options come up too often
    roll = random.randrange(1,6)
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
    
    if roll == 1:
        clearscreen()
        Player.find_gold()
        
    elif roll == 2:
        clearscreen()
        print "\nYou stepped on a booby trap!"
        Player.take_damage(random.randint(1,7))
        
    elif roll == 3:
        clearscreen()
        print "\nYou found a locked door..."
        if Player.has_key is True:
            print "\nYou opened it with the key that you found"
            Player.find_weapon()
        else:
            print "\nBut you can't open it since you don't have the key"
            sleep(2)
        
    elif roll == 4:
        clearscreen()
        print "\nYou stumbled upon a dead body, you look through it's backpack...."
        sleep(1)
        number = random.randint(0,3)
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
        clearscreen()
        monster_names = ["Gremlin", "Demon", "Zombie"]
        choice = random.choice(monster_names)
        if choice == "Gremlin":
            newMonster = monsters.CreateMonster(random.randint(10,15), random.randint(1,7),"Gremlin") #HP,damage_dealt,name
            newMonster.attack(Player)
            del newMonster
        
        elif choice == "Demon":
            newMonster = monsters.CreateMonster(random.randint(15,25), random.randint(7,15),"Demon") #HP,damage_dealt,name
            newMonster.attack(Player)
            del newMonster
        
        else:
            newMonster = monsters.CreateMonster(random.randint(25,35), random.randint(10,20),"Zombie") #HP,damage_dealt,name
            newMonster.attack(Player)
            del newMonster            
            
    else:
        clearscreen()
        print "\nYou're safe for the moment!"
        print "\nTake a minute to catch your breath"
        if Player.health <= 60 and Player.potions > 0:
            Player.low_health()
        sleep(2)
        
       
def visit_shop(Player):
    clearscreen()
    print "\nWhat would you like to purchase?"
    print "You currently have %d gold coins." % Player.gold
    print "\nP) Health Potions"
    print "W) Weapons"
    print "N) Nothing/Leave Store"
    choice = raw_input("\nChoice: ")
    choice.lower()
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
