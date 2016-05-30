#!/bin/python2
#
#~actions.py~

from time import sleep
from random import randint
from random import randrange
import os
import misc
import inventory

def roll_test_dice():
    counter = 0
    while counter < 10:
        rolls = []
        rolls.append(randint(1,6))
        counter +=1
        print "counter: %d" % counter
    print rolls
    sleep(5)

def roll_dice():
    global backpack
    #roll = randint(1,6)  #this is what is screwing up the dice rolling!
    roll = 5
    misc.clearscreen
    print "\nYou walked %d paces and..." % roll
    sleep(1)
    
    if roll == 1:
        misc.clearscreen()
        find_gold(randint(1,11))
        
    elif roll == 2:
        misc.clearscreen()
        print "\nYou were attacked by a Big Monster!\n"
        inventory.backpack["hp"] -= 15
        print "Your health is now at %d" % inventory.backpack["hp"]
        sleep(2)
        
    elif roll == 3:
        misc.clearscreen()
        print "You found a weapon!"
        sleep(2)
        
    elif roll == 4:
        misc.clearscreen()
        find_potion()
        
    elif roll == 5:
        misc.clearscreen()
        print "\nYou were attacked by a Small Monster!\n"
        inventory.backpack["hp"] -= 5
        print "Your health is now at %d" % inventory.backpack["hp"]
        sleep(2)
        
    else:
        misc.clearscreen()
        print "You're safe for the moment!"
        print "Take a minute to catch your breath"
        sleep(2)
        if inventory.inv[0] <= 60 and inventory.inv[1] > 0:
            print "\n*****DANGER*****\n"
            choice = raw_input("\nYour health is currently at %d, would you like to use a Health Potion? (y or n) " % inventory.inv[0])
            choice.lower()
            if choice == 'y':
                use_potion()
            else:
                print "\nOk tough guy."
       
def visit_shop():
    misc.clearscreen()
    print "\nWhat would you like to purchase?"
    print "You currently have %d gold coins." % inventory.inv[2]
    print "\nP) Health Potions"
    print "W) Weapons"
    print "N) Nothing"
    choice = raw_input("\nChoice: ")
    choice.lower()

    if choice == 'p':
        potions_amount = int(raw_input("\nEach Health Potion is 20 gold coins and restores 10 health. \nHow many would you like to buy?: "))
        if (potions_amount*20) <= inventory.inv[2]:
            print "\nYou have purchased %d Health Potions." % potions_amount
            inventory.inv[2] -= (potions_amount*20) #subtract the cost of the potions from the total gold
            inventory.inv[1] += potions_amount #add the purchased potions to the total held in inventory
            sleep(1)
        else:
            print "\nSorry you don't have enough gold!"
            sleep(1)
            visit_shop()
            
    elif choice == 'w':
        print "\nSorry we're currently out of weapons"
        sleep(1)
        
    elif choice == 'n':
        print "\nWhy did you come here then?!"
        sleep(1)
    
    else:
        print "Not a valid choice"
        sleep(1)
        
def find_gold(amount):
    global inv
    inventory.inv[2] = inventory.inv[2] + amount
    print "\nYou found %d gold! You now have %d pieces of gold!" % (amount,inventory.inv[2])
    sleep(1)
    
def quit_game():
    print "\nGood Bye!\n"
    exit(0)
    
def find_potion():
    global inv
    sleep(1)
    print "\nYou found a health potion."
    print "You now have %d health potions in your inventory." % inventory.inv[1]
    inventory.inv[1] += 1
    
def use_potion():
    global inv
    amount = int(raw_input("\nYou currently have %d health potions. \nHow many would you like to use?\n Each one restores 10 HP "))
    inventory.inv[0] += (amount*10)
    inventory.inv[2] -= amount
    print "\nYour health is now at %d" % inventory.inv[0]
