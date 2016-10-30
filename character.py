#!/usr/bin/python
#
#~character.py~

from superRandom import super_choice
from equipment import Equipment
from skills import Skill
from copy import deepcopy

class Character(object):
    '''
    This class will hold all battle methods needed by the
    Player and the ANPC classes
    '''

    def __init__(self, **build):
        self.name = build["name"]
        self.stats = {
                "hp": 100, #health points
                "max_hp": 100,
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
                #accuracy and evasion are only for use in battle
                #thus will never recieve an upgrade via lvl_up
                "acc": 100, #accuracy
                "eva": 100, #evasion
                "lvl": 1, #level
                "exp": 0, #experience
                "exp_needed": 200, #experience needed for next level
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
        self.skills = [""] * 5
        self.skill_bag = [] #holds the names of obtained, but unequipped skills

        #some lambda methods for simple functions
        self.check_if_dead = lambda: (True if not self.stats["hp"]
                else False)
        self.check_if_lucky = lambda: super_choice([
            super_choice((1,1,1,2)) for x in range(self.stats["lck"])
            ])

        self.build(build)

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
            self.equip_skill(skill)

        #inventory
        for item, quantity in inv.items():
            self.edit_inv(item, quantity)

        #stats
        for stat, amount in stats.items():
            if stat in self.stats:
                self.stats[stat] = amount
                if ("max_" + stat) in self.stats:
                    self.stats["max_" + stat] = amount
            #extrapolates stats from basis
            if self.stats["lvl"] - 1:
                lvl = self.stats["lvl"]
                self.stats["lvl"] = 1
                self.lvl_up(lvl)

    def stat_modifier(self, stat_mod, reverse = False):
        '''
        all stat modifications to the character will use this
        method

        stat_mod is a dictionary with the following syntax:
        {stat_to_be_modified:modification,...}

        the reverse flag is for when you want to divide or subtract
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
            elif "max" in stat:
                real_stat = stat[-2:]
                if self.stats[stat] != self.stats[real_stat]:
                    self.stats[real_stat] = self.stats[stat]
            if self.stats[stat] < 0:
                self.stats[stat] = 0

    def lvl_up(self, next_lvl = 0):
        '''
        used to lvl up characters
        '''

        current_lvl = self.stats["lvl"]
        if not next_lvl:
            next_lvl = current_lvl + 1
        if next_lvl > 100: #max lvl is 100
            return
        diff = next_lvl - current_lvl
        squared_diff = (next_lvl**2) - (current_lvl**2)
        hp_b = 18 #max hp possible is about 900 + base
        exp_m = 2 #max exp needed possible is about 10000
        other_stat_b = 6 #max other stat is about 290 + base
        lvl_func = (lambda m, b: (.5 * m * squared_diff) + (b * diff))

        valid_stats = ('max_hp','max_sp','max_mp','def',
                'str','md','ma','spe','lck','exp_needed')
        stat_mod_dict = {"lvl":diff}
        for stat in valid_stats:
            if 'hp' in stat:
                b = hp_b
                m = b / -101.0
            elif 'exp' in stat:
                m = exp_m
                b = 0
            else:
                b = other_stat_b
                m = b / -101.0
            stat_mod_dict[stat] = int(round(lvl_func(m,b)))
        self.stat_modifier(stat_mod_dict)
        if self.stats["lvl"] == 100: #lvl 100 is max
            self.stats["exp_needed"] = float("inf")

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

        #make string into Equipment object if not already
        if not isinstance(equipment, Equipment):
            equipment = Equipment(equipment)

        #manage inventory
        if (not dequip) and (equipment.name in self.inventory):
            self.edit_inv(equipment.name, 1, True)
        elif dequip and equipment.name not in ("bare", "claws"):
            self.edit_inv(equipment.name, 1)

        #apply or remove equipment mods
        self.stat_modifier(equipment.mods, dequip)

        #attach equipment to player
        if (equipment.equip_type == "armour" or
                equipment.hands_needed == 1):
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
            for h in ("right", "left"):
                if not dequip:
                    if self.equipment[h + "_hand"]:
                        self.equip(
                                self.equipment[h + "_hand"],
                                h + "_hand", True, True)
                    self.equipment[h + "_hand"] = equipment
                else:
                    self.equipment[h + "_hand"] = None
                    if not self_sent:
                        self.equip("bare", h + "_hand")

    def add_skill(self, skill_name, remove = False):
        '''
        This method handles adding and removing
        skills to and from skill bag
        '''

        if not remove:
            self.skill_bag.append(skill_name)
        else:
            self.skill_bag.remove(skill_name)

    def equip_skill(self, skill_name, dequip = False):
        '''
        method for equiping and dequiping skills
        '''

        if not dequip:
            if len(filter(lambda x: x, self.skills)) < 5:
                self.add_skill(skill_name, True)
                self.skills[self.skills.index("")] = skill_name
                return True
            else:
                return False
        else:
            self.skills[self.skills.index(skill_name)] = ""
            self.add_skill(skill_name)

    def edit_inv(self, item, quantity, remove = False):
        '''
        adds/removes items to/from inventory
        '''

        quantity = -quantity if remove else quantity
        if item in self.inventory:
            if remove and quantity == -self.inventory[item]:
                self.inventory.pop(item)
            else:
                self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def format_atk(self, atk, target_name = '', atk_name = ''):
        '''
        This handles the formatting the atk strings into
        a viewer friendly string
        '''

        if "target" not in atk or isinstance(atk["target"], str):
            atk["target"] = target_name
        else:
            target_name = 'target_name'
        atk = self.format_string_in_dict(atk, target_name, atk_name)
        return atk

    def format_string_in_dict(self, dic, target_name, atk_name):
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
                            else atk_name if word == 'atk_name'
                            else word)
                    new_str += after_word
                dic[key] = (new_str[:len(new_str) - 1] if
                        new_str[len(new_str) - 1] == ' ' else new_str)
        return dic
