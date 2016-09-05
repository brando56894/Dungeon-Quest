#!/usr/bin/python
#
#~character.py~

from superRandom import super_choice
from equipment import Equipment
from skills import skills
from copy import deepcopy

class Character(object):
    '''
    This class will hold all battle methods needed by the
    Player and the ANPC classes
    '''

    def __init__(self, **build):
        self.name = build["name"]
        self.stats = {
                "hp": 200, #health points
                "max_hp": 200,
                "sp": 10, #skill points
                "max_sp": 10,
                "mp": 10, #magic points
                "max_mp": 10,
                "def": 10, #defense
                "str": 10, #strength
                "md": 10, #magic defence
                "ma": 10, #magic attack
                "spe": 10, #speed
                "lck": 10, #luck
                "acc": 100, #accuracy
                "eva": 100, #evasion
                "lvl": 1, #level
                "exp": 0, #experience
                "gold": 0, #gold
                }
        self.inventory = {} #item:quantity
        self.equipment = {
                "head": None,
                "right_hand": None,
                "left_hand": None,
                "body": None,
                "legs": None
                }
        #This is the regular attack for all characters
        self.reg_atk = {
                "base_atk": 60,
                "base_acc": 95,
                "atk_str": "name attacked target_name!"
                }
        self.skills = {}

        #some lambda methods for simple functions
        self.check_if_dead = lambda: (True if not self.stats["hp"]
                else False)
        self.check_if_lucky = lambda: super_choice([
            super_choice((1,1,1,2)) for x in range(self.stats["lck"])
            ])

        self.build(build)

    def __repr__(self):
        pass

    def build(self, build):
        '''
        Uses the dictionary passed to it by __init__ to
        build the character to its current state

        current build composition:
            build = {
                "name": "name of character",
                "equipment": dictionary of equipment, {body_part: equipment}
                "skills": list of skills,
                "inventory": dictionary of items {item: quantity}
                "stats": dictionary of stats excluding max_X stats
            }
        '''
        equipment = build.get("equipment", {})
        skill_set = build.get("skills", [])
        inv = build.get("inventory", {})
        stats = build.get("stats", {})

        #equip
        for part, item in equipment.items():
            if "hand" not in part and item:
                self.equip(item, part)
            elif "hand" in part:
                self.equip(item if item else 'bare', part)

        #skills
        for skill in skill_set:
            self.add_skill(skill)

        #inventory
        for item, quantity in inv.items():
            self.edit_inv(item, quantity)

        #stats
        for stat, amount in stats.items():
            if stat in self.stats:
                self.stats[stat] = amount
                if ("max_" + stat) in self.stats:
                    self.stats["max_" + stat] = amount

    def stat_modifier(self, stat_mod, reverse = False):
        '''
        all stat modifications to the character will use this
        method

        stat_mod is a dictionary with the following syntax:
        {stat_to_be_modified:modification,...}
        '''

        for sM in stat_mod:
            stat = sM
            mod = stat_mod[stat]
            if not reverse:
                if isinstance(mod, float):
                    self.stats[stat] *= mod
                else:
                    self.stats[stat] += mod
            else:
                if isinstance(mod, float):
                    self.stats[stat] /= mod
                else:
                    self.stats[stat] -= mod
            if stat in ("hp", "mp", "sp"):
                if self.stats[stat] > self.stats["max_" +
                        stat]:
                    self.stats[stat] = self.stats["max_" +
                            stat]
            if self.stats[stat] < 0:
                self.stats[stat] = 0

    def SPMP_regen(self):
        '''
        Regenerate sp and mp after each
        turn at a reasonable rate
        '''

        for stat in ("mp", "sp"):
            full = self.stats["max_" + stat]
            now = self.stats[stat]
            lck = self.check_if_lucky()
            if not now:
                now += 1
            mod = int(round(lck * .25 * full / now))
            self.stat_modifier({stat:mod if mod else 1})

    def SPMP_handle(self, atk):
        '''
        Make sure character has enough sp or mp
        to use skill
        '''

        SPMP_needed = atk.get("mp_used", 0)
        if SPMP_needed:
            stat = "mp"
        else:
            SPMP_needed = atk.get("sp_used", 0)
            stat = "sp"
        if SPMP_needed > self.stats[stat]:
            return False
        self.stat_modifier({stat: -SPMP_needed})
        return True

    def equip(self, equipment, where_to_put,
            dequip = False, self_sent = False):
        '''
        This method handles detaching and attaching equipment

        self_sent boolean is for when the method calls itself

        where_to_put is irrelevent for 2 handed weapons so anything
        can be put there if the weapon in question needs 2 hands
        '''

        if not isinstance(equipment, Equipment):
            equipment = Equipment(equipment)
        self.stat_modifier(equipment.mods, dequip)
        if equipment.equip_type == "armour":
            if not dequip:
                if self.equipment[where_to_put]:
                    self.equip(self.equipment[where_to_put],
                            where_to_put, True, True)
                self.equipment[where_to_put] = equipment
            else:
                self.equipment[where_to_put] = None
                if "hand" in where_to_put and not self_sent:
                    self.equip("bare", where_to_put)
        else:
            hands_needed = equipment.hands_needed
            if not dequip:
                if hands_needed == 2:
                    for h in ("right", "left"):
                        if self.equipment[h + "_hand"]:
                            self.equip(
                                    self.equipment[h + "_hand"],
                                    h + "_hand", True, True)
                        self.equipment[h + "_hand"] = equipment
                else:
                    if self.equipment[where_to_put]:
                        self.equip(self.equipment[where_to_put],
                                where_to_put, True, True)
                    self.equipment[where_to_put] = equipment
            else:
                if hands_needed == 2:
                    for h in ("right", "left"):
                        if self_sent:
                            self.equipment[h + "_hand"] = None
                        else:
                            self.equip("bare", h + "_hand")
                else:
                    self.equipment[where_to_put] = None
                    if not self_sent:
                        self.equip("bare", where_to_put)
        if not self_sent:
            #clean up None values in hand
            for h in ("right", "left"):
                if not self.equipment[h + "_hand"]:
                    self.equip("bare", h + "_hand")

    def add_skill(self, skill_name, remove = False):
        '''
        This method handles adding and removing skills
        to and from character
        '''

        if not remove:
            for key, values in skills.items():
                if skill_name in values:
                    skill = skills[key][skill_name]
                    break
            self.skills[skill_name] = skill
        else:
            self.skills.pop(skill_name)

    def edit_inv(self, item, quantity, remove = False):
        quantity = -quantity if remove else quantity
        if item in self.inventory:
            if remove and quantity == -self.inventory[item]:
                self.inventory.pop(item)
            else:
                self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def format_atk(self, atk, target_name = ''):
        '''
        This handles the formatting the atk strings into
        a viewer friendly string
        '''

        if "target" not in atk or isinstance(atk["target"], str):
            atk["target"] = target_name
        else:
            target_name = 'target_name'
        atk = self.format_string_in_dict(atk, target_name)
        return atk

    def format_string_in_dict(self, dic, target_name):
        '''
        used to format strings in the atk dictionary

        currently does not work for atk_name and defaults
        to attack
        '''

        for key in dic:
            if isinstance(dic[key], dict):
                dic[key] = self.format_string_in_dict(dic[key], target_name)
            if (isinstance(dic[key], str) and
                    len(dic[key].split()) > 1):
                new_str = ''
                for word in dic[key].split():
                    after_word = ' '
                    for x in ("'s", "!"):
                        if x in word:
                            after_word = "%s " %(x)
                            word = word[:len(word) - len(x)]
                    new_str += (target_name if word == 'target_name'
                            else self.name if word == 'name'
                            else 'attack' if word == 'atk_name'
                            else word)
                    new_str += after_word
                dic[key] = (new_str[:len(new_str) - 1] if
                        new_str[len(new_str) - 1] == ' ' else new_str)
        return dic
