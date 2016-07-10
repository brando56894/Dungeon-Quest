#!/usr/bin/python2
#~~debug.py~~

"""
This will allow you to call functions
directly in order to test them out
"""

import player
import monsters
import actions
from time import sleep

def menu(newPlayer, newWeapon):
    actions.clearscreen()
    print "\n1. monster methods"
    print "2. player methods"
    print "3. actions functions"

    choice = raw_input("\nChoice: ")
    choice = choice.lower()
    
    if choice == "1":
        monster_methods(newPlayer, newWeapon)
    elif choice == "2":
        player_methods(newPlayer)
    elif choice == "3":
        actions_functions(newPlayer)
    else:
        print "Not a valid choice"
        sleep(2)
    return
    
def monster_methods(newPlayer, newWeapon):
    print "\n1. create()"
    print "2. take_damage()"
    print "3. deal_damage()"
    print "4. attack()"
    
    choice = raw_input("\nWhich method? ")
    
    if choice == '1':
        newMonster = monsters.create(25,15,"Big Monster") #(HP,damage_dealt,name)
        print "Created %s that deals %d damage and has %d health" % (newMonster.name,newMonster.damage_dealt,newMonster.health)
        sleep(2)
    elif choice == '2':
        newMonster = monsters.create(25,15,"Big Monster")
        damage = int(raw_input("How much? "))
        newMonster.take_damage(damage,newPlayer)
    elif choice == '3':
        newMonster = monsters.create(25,15,"Big Monster")
        #damage = int(raw_input("How much? ")) 
        newMonster.deal_damage(newPlayer)
    elif choice == '4':
        newMonster = monsters.create(25,15,"Big Monster")
        newMonster.attack(newPlayer, newWeapon)
    else:
        print "Not a valid choice"
        sleep(2)
    return
    
def player_methods(newPlayer):
    print "\n1. find_gold()"
    print "2. find_gold_debug()"
    print "3. find_potions()"
    print "4. find_weapon()"
    print "5. use_potion()"
    print "6. list_inventory()"
    print "7. low_health()"
    print "8. set_health()"
    print "9. take_damage()"
    print "10. deal_damage()"
    print "11. gain_xp()"
    print "12. add_weapon()"
    print "13. buy_weapon()"
    print "14. set_current_weapon()"
    print "15. set step count"
    
    choice = raw_input("\nWhich method? ")
    
    if choice == '1':
        newPlayer.find_gold()
    elif choice == '2':
        amount = int(raw_input("How much? "))
        newPlayer.find_gold_debug(amount)
    elif choice == '3':
        newPlayer.find_potions()
    elif choice == '4':
        newPlayer.find_weapon()
    elif choice == '6':
        newPlayer.list_inventory()
    elif choice == '7':
        newPlayer.low_health()
    elif choice == '8':
        health = int(raw_input("To what? "))
        newPlayer.set_health(health)
    elif choice == '9':
        damage = int(raw_input("How much? "))
        newPlayer.take_damage(damage)
    elif choice == '10':
        damage = int(raw_input("How much? "))
        newPlayer.deal_damage(damage)        
    elif choice == '11':
        monster = raw_input("Which monster did you kill? ")
        newPlayer.gain_xp(monster)
    elif choice == '12':
        name = raw_input("Weapon name? ")
        damage = raw_input("Weapon damage? ")
        newPlayer.add_weapon(name,damage)
    elif choice == '13':
        newPlayer.buy_weapon()
    elif choice == '14':
        newPlayer.set_current_weapon()
    elif choice == '15':
        steps = int(raw_input("To what? "))
        newPlayer.steps = steps
        print "Step count set to %d" % newPlayer.steps
        sleep(2)
    else:
        print "Not a valid choice"
        sleep(2)
    return
        
def actions_functions(newPlayer):
    print "\n1. roll_dice()"
    print "2. visit_shop()"
    
    choice = raw_input("\nWhich function? ")
    
    if choice == '1':
        actions.roll_dice()
    elif choice == '2':
        actions.visit_shop()
    else:
        print "Not a valid choice"
        sleep(2)
    return    
