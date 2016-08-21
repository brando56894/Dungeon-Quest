#!/usr/bin/python
#
#~weapons.py~

#general attack strings
meleeGenAtkString = "name attacked targetName!"
rangedGenAtkString = "name fired at targetName!"

#weapon definitions
weapons = {
        "sword": {
            "type": "blade",
            "mod": {"str": 10, "def": 5},
            },
        "pistol": {
            "type": "gun",
            "mod": {"str": 15, "def": -5},
            },
        "rifle": {
            "type": "gun",
            "mod": {"str": 30, "def": -5, "spe": -5},
            },
        "dagger": {
            "type": "blade",
            "mod": {"str": 5, "spe": 5, "lck": 5},
            },
        "bow": {
            "type": "bow",
            "mod": {"str": 10, "spe": 5},
            },
        "crossbow": {,
            "type": "bow",
            "mod": {"str": 20, "spe": 5},
            },
        "staff": {,
            "type": "staff",
            "mod": {"ma": 10, "md": 10},
            },
        "gauntlet": {
            "type": "fist",
            "mod": {"str": 10, "def": -10, "spe": 5},
            },
        "bare": {
            "type": "fist",
            "mod": {"spe": 10},
            },
        }

class Weapon(object):

    def __init__(self, name):
        self.name = name
        self.type = ""
        self.regAtk = {}
        self.build()

    def build(self):
        self.type = weapons[self.name]["type"]
        decideString = lambda x: (meleeGenAtkString if x 
                in ("fist", "blade", "staff") else
                rangedGenAtkString)
        self.regAtk = {
                "baseAtk": 50,
                "baseAcc": 95,
                "atkString": decideString(self.type)
                }
        self.mods = weapons[self.name]["mod"]
