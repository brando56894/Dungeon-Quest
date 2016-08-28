#!/usr/bin/python
#
#~charANPC.py~

from superRandom import super_choice
from equipment import Equipment
from skills import skills
from copy import deepcopy

class CharANPC(object):

    def __init__(self, build):
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
                "exp": 0, #experience
                "gol": 0, #gold
                }
        self.lvl = 1
        self.inventory = {}
        self.equipment = {
                "head": None,
                "right_hand": None,
                "left_hand": None,
                "body": None,
                "legs": None
                }
        self.reg_atk = {
                "base_atk": 60,
                "base_acc": 95,
                "atk_str": "name attacked target_name!"
                }
        self.skills = {"reg_atk": self.reg_atk}
        self.check_if_dead = lambda: (True if not self.stats["hp"]
                else False)
        self.check_if_lucky = lambda: super_choice([
            super_choice((1,1,1,2)) for x in range(self.stats["lck"])
            ])
        self.build(build)

    def build(self, build):
        self.name = build["name"]
        equipment = build.get("equipment", {})
        skill_set = build.get("skills", {})
        for hand in ("right_hand", "left_hand"):
            self.equip(build["equipment"].get(hand, "bare"), hand)
        for part, item in equipment.items():
            if part not in ("right_hand", "left_hand") and item:
                self.equip(item, part)
            elif part in ("right_hand", "left_hand"):
                self.equip(item if item else 'bare', part)
        for skill in skill_set:
            self.add_skill(skill)

    def stat_modifier(self, stat_mod, reverse = False):
        '''
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
                elif self.stats[stat] < 0:
                    self.stats[stat] = 0

    def SPMP_regen(self):
        for stat in ("mp", "sp"):
            full = self.stats["max_" + stat]
            now = self.stats[stat]
            lck = self.check_if_lucky()
            if not now:
                now += 1
            mod = lck * .25 * full / now
            self.stat_modifier({stat:mod})

    def SPMP_handle(self, atk):
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
        #self_sent boolean is for when the method calls itself
        #where_to_put is irrelevent for 2 handed weapons so anything
        #can be put there if the weapon in question needs 2 hands

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
                                    where_to_put, True, True)
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

    def add_skill(self, skill_name):
        for key, values in skills.items():
            if skill_name in values:
                skill = skills[key][skill_name]
                break
        self.skills[skill_name] = skill

    def format_atk(self, atk, target_name = ''):
        if "target" not in atk or isinstance(atk["target"], str):
            atk["target"] = target_name
        else:
            target_name = 'target_name'
        atk = self.format_string_in_dict(atk, target_name)
        return atk

    def format_string_in_dict(self, dic, target_name):
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
                            else 'reg_atk' if word == 'atk_name'
                            else word)
                    new_str += after_word
                dic[key] = (new_str[:len(new_str) - 1] if
                        new_str[len(new_str) - 1] == ' ' else new_str)
        return dic



class Player(CharANPC):
    pass

class ANPC(CharANPC):
    
    def AI_atk(self, allies, enemies):
        if self.name in allies:
            not_team = enemies
        not_team = allies if self.name not in allies else enemies
        skill = super_choice(self.skills.values())
        atk = skill if self.SPMP_handle(skill) else self.reg_atk
        return self.format_atk(deepcopy(atk), super_choice(not_team))
