#!/usr/bin/python
#
#~equipment.py~

#weapon definitions
weapons = {
    "sword": {
        "type": "blade",
        "mods": {"str": 5, "def": 3},
        "handsNeeded": 1,
        },
    "pistol": {
        "type": "gun",
        "mods": {"str": 8, "def": -3},
        "handsNeeded": 1,
        },
    "rifle": {
        "type": "gun",
        "mods": {"str": 30, "def": -5, "spe": -5},
        "handsNeeded": 2,
        },
    "dagger": {
        "type": "dagger",
        "mods": {"str": 3, "spe": 3, "lck": 3},
        "handsNeeded": 1,
        },
    "bow": {
        "type": "bow",
        "mods": {"str": 10, "spe": 5},
        "handsNeeded": 2,
        },
    "crossbow": {
        "type": "bow",
        "mods": {"str": 20, "spe": 5},
        "handsNeeded": 2,
        },
    "staff": {
        "type": "staff",
        "mods": {"ma": 5, "md": 5},
        "handsNeeded": 1,
        },
    "gauntlet": {
        "type": "fist",
        "mods": {"str": 5, "def": -5, "spe": 3},
        "handsNeeded": 1,
        },
    "bare": {
        "type": "fist",
        "mods": {"spe": 5},
        "handsNeeded": 1,
        },
    }

#armour definitions
armour = {
    "cap":{
        "type": "head",
        "mods":{"def": 1},
        },
    "wooden shield":{
        "type": "hand",
        "mods":{"def": 2},
        },
    "rusty chainmail":{
        "type": "body",
        "mods":{"def": 5},
        },
    "leather greaves":{
        "type": "legs",
        "mods":{"def": 1},
        },
    }

class Equipment(object):

    def __init__(self, name):
        self.name = name
        self.equipType = ("armour" if name in armour
                else "weapon")
        self.build()

    def build(self):
        if self.equipType == "armour":
            defDict = armour
        else:
            defDict = weapons
            self.handsNeeded = defDict[self.name][
                    "handsNeeded"]
        self.type = defDict[self.name]["type"]
        self.mods = defDict[self.name]["mods"]
