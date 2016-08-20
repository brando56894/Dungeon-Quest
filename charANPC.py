#!/usr/bin/python
#
#~charANPC.py~

from superRandom import superChoice

class charANPC(object):

    def __init__(self):
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
                "lck": 10 #luck
                }
        self.lvl = 1
        self.inventory = {}
        self.equipment = []

    def statModifier(self, statMod):
        '''
        statMod is a dictionary with the following syntax:
        {stat_to_be_modified:modification,...}
        '''

        for sM in statMod:
            stat = sM
            mod = statMod[stat]
            if isinstance(mod, float):
                statMod[stat] *= mod
            else:
                statMod[stat] += mod
            if stat in ("hp", "mp", "sp"):
                if self.stats[stat] > self.stats["max" + stat.upper()]:
                    self.stats[stat] = self.stats["max" + stat.upper()]
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

    def checkIfDead(self):
        if self.stats["hp"] == 0:
            return True
        return False

    def checkIfLucky(self):
        return superChoice([superChoice([1,2]) for
            x in range(self.stats["lck"])])
