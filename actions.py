#!/bin/python2
#
#~actions.py~

from time import sleep
from random import randint
import os
import monsters

def roll_dice(newPlayer):
    #TODO: add more roles since some options come up too often, also try to find a better random number generator
    roll = randint(1,6)
    clearscreen
    if roll == 1:
        print "\nYou walked %d pace and..." % roll
    else:
        print "\nYou walked %d paces and..." % roll
    sleep(1)
    
    if roll == 1:
        clearscreen()
        newPlayer.find_gold()
        
    elif roll == 2:
        clearscreen()
        newMonster = monsters.create(50,15,"Big Monster") #creates a monster named 'Big Monster' with 50 HP that deals 15 damage per hit
        newMonster.attack(newPlayer)
        del newMonster
        
    elif roll == 3:
        clearscreen()
        newPlayer.find_weapon() #TODO: make this actually do something
        
    elif roll == 4:
        clearscreen()
        newPlayer.find_potions()
        
    elif roll == 5:
        clearscreen()
        newMonster = monsters.create(25,7,"Small Monster") #creates a monster named 'Small Monster' with 25 HP that deals 7 damage per hit
        newMonster.attack(newPlayer)
        del newMonster
        
    else:
        clearscreen()
        print "\nYou're safe for the moment!"
        print "Take a minute to catch your breath"
        if newPlayer.health <= 60 and newPlayer.potions > 0:
            newPlayer.low_health()
        sleep(2)
        
       
def visit_shop(newPlayer):
    clearscreen()
    print "\nWhat would you like to purchase?"
    print "You currently have %d gold coins." % newPlayer.gold
    print "\nP) Health Potions"
    print "W) Weapons"
    print "N) Nothing"
    choice = raw_input("\nChoice: ")
    choice.lower()

    if choice == 'p':
        newPlayer.buy_potions()
                    
    elif choice == 'w':
        #TODO: implement a purchase_weapon() function
        print "\nSorry we're currently out of weapons"
        sleep(2)
        visit_shop()
        
    elif choice == 'n':
        print "\nWhy did you come here then?!"
        sleep(2)
        return
    
    else:
        print "Not a valid choice"
        sleep(2)
        visit_shop()
    
def quit_game():
    print "\nGood Bye!\n"
    exit(0)
    
def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')
