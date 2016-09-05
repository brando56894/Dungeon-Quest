#!/usr/bin/python2
#
#~~ANPC.py~~

from time import sleep
from superRandom import super_choice
from character import Character
from copy import deepcopy
import battle

monsters = {
        "gremlin": {
            "equipment": {
                "head": "cap",
                "body": "rusty chainmail",
                "legs": "leather greaves",
                "right_hand": "dagger",
                "left_hand": "dagger"
                },
            "skills": ["smokescreen", "backstab",
                "vampire strike"],
            "inventory": {"potion": 1},
            #default stats are in character.py
            #any stat not included except for the max_X stats will be
            #given default value
            "stats": {
                "hp": 30,
                "def": 5,
                "str": 5,
                "md": 5,
                "ma": 5,
                "spe": 15,
                "lck": 15,
                "exp": 20, #base exp given during reward phase of battle
                "gold": 10 #base gold given during reward phase of battle
                }
            },
        "demon": {
            "equipment": {
                "head": "cap",
                "body": "rusty chainmail",
                "legs": "leather greaves",
                "right_hand": "wooden shield",
                "left_hand": "sword"
                },
            "skills": ["trip", "shield bash",
                "counter strike"],
            "inventory": {"potion": 1},
            "stats": {
                "hp": 70,
                "exp": 50,
                "gold": 30
                }
            },
        "zombie": {
            "equipment": {
                "head": "cap",
                "body": "rusty chainmail",
                "legs": "leather greaves",
                "right_hand": "bare",
                "left_hand": "gauntlet"
                },
            "skills": ["speed punch", "trip", "warcry"],
            "inventory": {"potion": 1},
            "stats": {
                "hp": 100,
                "def": 15,
                "str": 15,
                "spe": 5,
                "lck": 5,
                "exp": 100,
                "gold": 75
                }
            },
        "dragon": {
            "equipment": {
                #leaving out parts defaults those parts to None
                "body": "tough skin",
                "right_hand": "claws",
                "left_hand": "claws"
                },
            "skills": ["fireball"],
            "inventory": {"potion": 2},
            "stats": {
                "hp": 250,
                "sp": 30,
                "mp": 30,
                "def": 25,
                "str": 20,
                "md": 20,
                "ma": 20,
                "lck": 1,
                "exp": 200,
                "gold": 150
                }
            },
        "basilisk": {
            "equipment": {
                "body": "tough skin",
                "right_hand": "claws",
                "left_hand": "claws"
                },
            "skills": [],
            "inventory": {"potion": 3},
            "stats": {
                "hp": 350,
                "sp": 50,
                "mp": 50,
                "def": 30,
                "str": 35,
                "md": 10,
                "ma": 10,
                "spe": 1,
                "lck": 1,
                "exp": 300,
                "gold": 250
                }
            }
        }

class ANPC(Character):
    '''
    ANPC stands for Active Non Player Character

    This class will be used for any NPC in battle
    '''
    def build(self, build):
        if self.name in monsters:
            build = monsters[self.name]
        super(ANPC, self).build(build)

    def AI_atk(self, allies, enemies):
        '''
        This will be the method of attack for all ANPC's

        currently is random
        '''

        if self.name in allies:
            not_team = enemies
        not_team = allies if self.name not in allies else enemies
        skills = self.skills.values()
        skills.append(self.reg_atk)
        skill = super_choice(skills)
        atk = skill if self.SPMP_handle(skill) else self.reg_atk
        return self.format_atk(deepcopy(atk), super_choice(not_team))

def monster_appearance(player, boss = False):
    import main
    if boss:
        if player.stats["dragon_attack"]:
            monster = "basilisk"
        else:
            monster = "dragon"
        print ("\nA %s blocks your path! There looks to "
                "be no way around it.\n\nPrepare to fight!"
                % monster)
        can_run = False
    else:
        monster = super_choice(["gremlin", "demon", "zombie"])
        print "\nYou were attacked by a %s!" % monster
        can_run = True
    main.confirm()
    battle.battle(player, enemies = [ANPC(name = monster)], can_run = can_run) 
