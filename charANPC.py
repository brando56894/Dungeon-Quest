#!/usr/bin/python
#
#~charANPC.py~

from superRandom import superChoice
from equipment import Equipment

class CharANPC(object):

    def __init__(self, build):
        self.stats = {
                "hp": 10, #health points
                "maxHP": 10,
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
                "atkString": "name attacked targetName!"
                }
        self.skills = []
        self.checkIfDead = lambda: (True if not self.stats["hp"]
                else False)
        self.checkIfLucky = lambda: superChoice([
            superChoice((1,2)) for x in range(self.stats["lck"])
            ])
        self.build(build)

    def build(self, build):
        self.name = build["name"]
        for hand in ("rightHand", "leftHand"):
            self.equip(build["equipment"].pop(hand, "bare"), hand)

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

    def spRegen(self):
        full = stats["maxSP"]
        now = stats["sp"]
        lck = checkIfLucky()
        if not now:
            now += 1
        mod = lck * .25 * full / now
        self.statModifier({"sp":mod})

    def spHandle(self, skill):
        pass

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
