#!/usr/bin/python
#
#~charANPC.py~

from superRandom import superChoice
from equipment import Equipment
from skills import skills
from copy import deepcopy

class CharANPC(object):

    def __init__(self, build):
        self.stats = {
                "hp": 200, #health points
                "maxHP": 50,
                "sp": 10, #skill points
                "maxSP": 10,
                "mp": 10, #magic points
                "maxMP": 10,
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
                "rightHand": None,
                "leftHand": None,
                "body": None,
                "legs": None
                }
        self.regAtk = {
                "baseAtk": 60,
                "baseAcc": 95,
                "atkStr": "name attacked targetName!"
                }
        self.skills = {"regAtk": self.regAtk}
        self.checkIfDead = lambda: (True if not self.stats["hp"]
                else False)
        self.checkIfLucky = lambda: superChoice([
            superChoice((1,1,1,2)) for x in range(self.stats["lck"])
            ])
        self.build(build)

    def build(self, build):
        self.name = build["name"]
        equipment = build.get("equipment", {})
        skillSet = build.get("skills", {})
        for hand in ("rightHand", "leftHand"):
            self.equip(build["equipment"].get(hand, "bare"), hand)
        for part, item in equipment.items():
            if part not in ("rightHand", "leftHand") and item:
                self.equip(item, part)
            elif part in ("rightHand", "leftHand"):
                self.equip(item if item else 'bare', part)
        for part, skillList in skillSet.items():
            for skill in skillList:
                self.addSkill(part, skill)

    def statModifier(self, statMod, reverse = False):
        '''
        statMod is a dictionary with the following syntax:
        {stat_to_be_modified:modification,...}
        '''

        for sM in statMod:
            stat = sM
            mod = statMod[stat]
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
                if self.stats[stat] > self.stats["max" +
                        stat.upper()]:
                    self.stats[stat] = self.stats["max" +
                            stat.upper()]
                elif self.stats[stat] < 0:
                    self.stats[stat] = 0

    def SPMPRegen(self):
        for stat in ("mp", "sp"):
            full = self.stats["max" + stat.upper()]
            now = self.stats[stat]
            lck = self.checkIfLucky()
            if not now:
                now += 1
            mod = lck * .25 * full / now
            self.statModifier({stat:mod})

    def SPMPHandle(self, atk):
        SPMPNeeded = atk.get("mpUsed", 0)
        if SPMPNeeded:
            stat = "mp"
        else:
            SPMPNeeded = atk.get("spUsed", 0)
            stat = "sp"
        if SPMPNeeded > self.stats[stat]:
            return False
        self.statModifier({stat: -SPMPNeeded})
        return True

    def equip(self, equipment, whereToPut,
            dequip = False, selfSent = False):
        #selfSent boolean is for when the method calls itself
        #whereToPut is irrelevent for 2 handed weapons so anything
        #can be put there if the weapon in question needs 2 hands

        if not isinstance(equipment, Equipment):
            equipment = Equipment(equipment)
        self.statModifier(equipment.mods, dequip)
        if equipment.equipType == "armour":
            if not dequip:
                if self.equipment[whereToPut]:
                    self.equip(self.equipment[whereToPut],
                            whereToPut, True, True)
                self.equipment[whereToPut] = equipment
            else:
                self.equipment[whereToPut] = None
                if "Hand" in whereToPut and not selfSent:
                    self.equip("bare", whereToPut)
        else:
            handsNeeded = equipment.handsNeeded
            if not dequip:
                if handsNeeded == 2:
                    for h in ("right", "left"):
                        if self.equipment[h + "Hand"]:
                            self.equip(
                                    self.equipment[h + "Hand"],
                                    whereToPut, True, True)
                            self.equipment[h + "Hand"] = equipment
                else:
                    if self.equipment[whereToPut]:
                        self.equip(self.equipment[whereToPut],
                                whereToPut, True, True)
                    self.equipment[whereToPut] = equipment
            else:
                if handsNeeded == 2:
                    for h in ("right", "left"):
                        if selfSent:
                            self.equipment[h + "Hand"] = None
                        else:
                            self.equip("bare", h + "Hand")
                else:
                    self.equipment[whereToPut] = None
                    if not selfSent:
                        self.equip("bare", whereToPut)

    def addSkill(self, weapon, skillName):
        skill = skills[weapon][skillName]
        self.skills[skillName] = skill

    def formatAtk(self, atk, targetName = ''):
        if "target" not in atk or isinstance(atk["target"], str):
            atk["target"] = targetName
        else:
            targetName = 'targetName'
        atk = self.formatStringInDict(atk, targetName)
        return atk

    def formatStringInDict(self, dic, targetName):
        for key in dic:
            if isinstance(dic[key], dict):
                dic[key] = self.formatStringInDict(dic[key], targetName)
            if (isinstance(dic[key], str) and
                    len(dic[key].split()) > 1):
                newStr = ''
                for word in dic[key].split():
                    afterWord = ' '
                    for x in ("'s", "!"):
                        if x in word:
                            afterWord = "%s " %(x)
                            word = word[:len(word) - len(x)]
                    newStr += (targetName if word == 'targetName'
                            else self.name if word == 'name'
                            else 'regAtk' if word == 'atkName'
                            else word)
                    newStr += afterWord
                dic[key] = (newStr[:len(newStr) - 1] if
                        newStr[len(newStr) - 1] == ' ' else newStr)
        return dic



class Player(CharANPC):
    pass

class ANPC(CharANPC):
    
    def AIAtk(self, allies, enemies):
        if self.name in allies:
            notTeam = enemies
        notTeam = allies if self.name not in allies else enemies
        skill = superChoice(self.skills.values())
        atk = skill if self.SPMPHandle(skill) else self.regAtk
        return self.formatAtk(deepcopy(atk), superChoice(notTeam))
