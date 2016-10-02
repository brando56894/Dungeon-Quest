#!/usr/bin/python2
#~~debug.py~~
#This will allow you to call functions directly in order to test them out


import player
#import monsters
import actions
import main
from time import sleep

def menu(Player):
    main.clearscreen()
    print ("\n1. monster methods\n"
            "2. player methods\n"
            "3. actions functions")

    choice = raw_input("\nChoice: ").lower()
    
    if choice == "1":
        monster_methods(Player)
    elif choice == "2":
        player_methods(Player)
    elif choice == "3":
        actions_functions(Player)
    else:
        print "Not a valid choice"
        sleep(2)
    return
    
def monster_methods(Player):
    print ("\n1. create()\n"
            "2. take_damage()\n"
            "3. deal_damage()\n"
            "4. attack()\n"
            "5. Monster object attributes")
    
    choice = raw_input("\nWhich method? ")
    
    if choice == '1':
        Monster = monsters.CreateMonster(25,15,"Big Monster") #(HP,damage_dealt,name)
        print "Created %s that deals %d damage and has %d health" % (Monster.name,Monster.damage_dealt,Monster.health)
        sleep(2)
    elif choice == '2':
        Monster = monsters.CreateMonster(25,15,"Big Monster")
        damage = int(raw_input("How much? "))
        Monster.take_damage(damage,Player)
    elif choice == '3':
        Monster = monsters.CreateMonster(25,15,"Big Monster")
        #damage = int(raw_input("How much? ")) 
        Monster.deal_damage(Player)
    elif choice == '4':
        Monster = monsters.CreateMonster(25,15,"Big Monster")
        Monster.attack(Player)
    elif choice == '5':
        Monster = monsters.CreateMonster(25,15,"Big Monster")
        print Monster
        sleep(3)
    else:
        print "Not a valid choice"
        sleep(2)
    return
    
def player_methods(Player):
    print ("\n1. find_gold()\n"
            "2. find_gold_debug()\n"
            "3. find_potions()\n"
            "4. find_weapon()\n"
            "5. use_potion()\n"
            "6. list_inventory()\n"
            "7. low_health()\n"
            "8. set_health()\n"
            "9. take_damage()\n"
            "10. deal_damage()\n"
            "11. gain_xp()\n"
            "12. add_weapon()\n"
            "13. buy_weapon()\n"
            "14. set_current_weapon()\n"
            "15. set step count\n"
            "16. Player object attributes")
    
    choice = raw_input("\nWhich method? ")
    
    if choice == '1':
        Player.find_gold()
    elif choice == '2':
        amount = int(raw_input("\nHow much? "))
        Player.find_gold_debug(amount)
    elif choice == '3':
        Player.find_potions()
    elif choice == '4':
        Player.find_weapon()
    elif choice == '6':
        Player.list_inventory()
    elif choice == '7':
        Player.low_health()
    elif choice == '8':
        health = int(raw_input("\nTo what? "))
        Player.set_health(health)
    elif choice == '9':
        damage = int(raw_input("\nHow much? "))
        Player.take_damage(damage)
    elif choice == '10':
        damage = int(raw_input("\nHow much? "))
        Player.deal_damage(damage)        
    elif choice == '11':
        monster = raw_input("\nWhich monster did you kill? ")
        Player.gain_xp(monster)
    elif choice == '12':
        name = raw_input("\nWeapon name? ")
        damage = raw_input("Weapon damage? ")
        Player.add_weapon(name,damage)
    elif choice == '13':
        Player.buy_weapon()
    elif choice == '14':
        Player.set_current_weapon(Weapon)
    elif choice == '15':
        steps = int(raw_input("\nTo what? "))
        Player.steps = steps
        print "Step count set to %d" % Player.steps
        sleep(2)
    elif choice == '16':
        print Player
        sleep(9)
    else:
        print "\nNot a valid choice"
        sleep(2)
    return
        
def actions_functions(Player):
    print ("\n1. roll_dice()\n"
            "2. visit_shop()")
    
    choice = raw_input("\nWhich function? ")
    
    if choice == '1':
        actions.roll_dice(Player)
    elif choice == '2':
        actions.visit_shop()
    else:
        print "Not a valid choice"
        sleep(2)
    return    
