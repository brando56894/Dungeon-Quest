#!/usr/bin/python2
#
#~~ANPC.py~~

from time import sleep
from superRandom import super_choice
from character import Character
import actions

monsters = {
        #equipment, skills, inventory, stats
        "gremlin": {},
        "demon": {},
        "zombie": {},
        "dragon": {},
        "basilisk": {}
        }

class ANPC(Character):
    '''
    ANPC stands for Active Non Player Character

    This class will be used for any NPC in battle
    '''
    def build(self, build):
        super(ANPC, self).build(self, build)
        if not self.inventory:
            self.make_inv()

    def make_inv(self):
        pass

    def AI_atk(self, allies, enemies):
        '''
        This will be the method of attack for all ANPC's

        currently is random
        '''

        if self.name in allies:
            not_team = enemies
        not_team = allies if self.name not in allies else enemies
        skill = super_choice(self.skills.values())
        atk = skill if self.SPMP_handle(skill) else self.reg_atk
        return self.format_atk(deepcopy(atk), super_choice(not_team))

def monsterAppearance(player, boss = False):
    if boss:
        if player.stats["dragon_attack"]:
            monster = "basilisk"
        else:
            monster = "dragon"
        print ("\nA %s blocks your path! There looks to "
                "be no way around it.\n\nPrepare to fight!"
                % monster)
        #cant run
    else:
        monster = super_choice(["gremlin", "demon", "zombie"])
        print "\nYou were attacked by a %s!" % monster
        #can run
