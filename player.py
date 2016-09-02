#!/usr/bin/python2
#
#~~Player Functions~~

from superRandom import super_randint, super_choice
from time import sleep
import actions
import monsters
from charANPC import CharANPC

class Player(CharANPC):
  
    def __repr__(self):
        first_part = super(Player, self).__repr__(self)
        second_part = "Steps: %d\nTimes Run Away: %d" %(
                self.stats["steps"], self.stats["run_away"])
        return first_part + second_part

    def build(self, build):
        super(Player, self).build(build)
        for key in ("steps", "run_away", "dragon_attack",
                "basilisk_attack"):
            self.stats[key] = build.get(key, 0)

    #make a more general use item
    def use_potion(self): #*
        if self.potions > 0 and self.potions < 2:
            self.potions -= 1
            self.health += 25
            print "\nYour health is now at %d" % self.health
        elif self.potions > 1:
            print "\nYou currently have %d potions" % self.potions
            amount = int(raw_input("\nHow many? "))
            raise_health = amount * 25
            self.health += raise_health
            self.potions -= amount
            print "\nYour health is now at %d" % self.health
        else:
            print "\nSorry you don't have any more potions!"
        sleep(2)
        return self
        
    #make more general list_anything
    def list_inventory(self): #*
        actions.clearscreen()
        print ("\nName: %s\n"
                "Exp. Points: %d\n"
                "Potions Held: %d\n"
                "Gold: %d pieces\n"
                "Current Weapon: %s" %(self.name, self.xp,
                    self.potions, self.gold, self.current_weapon)
                )
        
        if self.has_pistol is True and "pistol" not in self.weapons:
            self.weapons.append("pistol")
        elif self.has_rifle is True and "rifle" not in self.weapons:
            self.weapons.append("rifle")
        elif self.has_sword is True and "sword" not in self.weapons:
            self.weapons.append("sword") 
        print "Weapons: %s" % ", ".join(str(weapon) for weapon in self.weapons)
        sleep(4)
        
    def low_health(self): #*
        if self.health <= 60 and self.potions > 0:
            print "\n*****DANGER*****\n"
            choice = raw_input("\nYour health is currently at %d, a"
                    "nd you currently have %d potions in your inven"
                    "tory. \nWould you like to use one? " % (self.health,self.potions)
                    )
            choice.lower()
            if choice == 'y' or choice == 'yes':
                self.use_potion()
                return self
            else:
                print "\nOk tough guy."
                sleep(2)
                return self
    
