#!/bin/python2
#
#~actions.py~

from time import sleep
from random import randint
from random import randrange
import os

def roll_dice(newPlayer):
    roll = randint(1,6)
    clearscreen
    print "\nYou walked %d paces and..." % roll
    sleep(1)
    
    if roll == 1:
        clearscreen()
        newPlayer.find_gold()
        
    elif roll == 2:
        clearscreen()
        print "\nYou were attacked by a Big Monster!\n"
        newPlayer.take_damage(15)
        sleep(2)
        
    elif roll == 3:
        clearscreen()
        newPlayer.find_weapon()
        
    elif roll == 4:
        clearscreen()
        newPlayer.find_potions()
        
    elif roll == 5:
        clearscreen()
        print "\nYou were attacked by a Small Monster!\n"
        newPlayer.take_damage(5)
        sleep(2)
        
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
