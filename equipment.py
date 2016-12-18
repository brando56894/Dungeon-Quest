#!/usr/bin/python
#
#~equipment.py~

#calculate cost based on mods
calc_cost = lambda atk: reduce(lambda x,y: x + y, atk["mods"].values()) * 10

#weapon definitions
weapons = {
    "blade": {
        "sword": {
            "mods": {"str": 7, "def": 3},
            "hands_needed": 1,
            },
        },
    "shield": {
        "wooden shield":{
            "mods":{"def": 2},
            "hands_needed": 1,
            },
        },
    "gun": {
        "pistol": {
            "mods": {"str": 8, "def": -3},
            "hands_needed": 1,
            },
        "rifle": {
            "mods": {"str": 15, "def": -5, "spe": -5},
            "hands_needed": 2,
            },
        },
    "dagger": {
        "dagger": {
            "mods": {"str": 3, "spe": 3, "lck": 3},
            "hands_needed": 1,
            },
        },
    "bow": {
        "bow": {
            "mods": {"str": 10, "spe": 5},
            "hands_needed": 2,
            },
        "crossbow": {
            "mods": {"str": 12, "spe": 5},
            "hands_needed": 2,
            },
        },
    "staff": {
        "staff": {
            "mods": {"ma": 5, "md": 5},
            "hands_needed": 1,
            },
        },
    "fist": {
        "gauntlet": {
            "mods": {"str": 10, "def": -5, "spe": 3},
            "hands_needed": 1,
            },
        "bare": {
            "mods": {"spe": 5},
            "hands_needed": 1,
            "no_shop": True #this tag makes the item not appear in shop
            },
        "claws": {
            "mods": {"str": 10, "spe": 10},
            "hands_needed": 1,
            "no_shop": True
            },
        }
    }

#armour definitions
armour = {
    "head": {
        "cap":{
            "mods":{"def": 1},
            },
        },
    "body": {
        "rusty chainmail":{
            "mods":{"def": 5},
            },
        "tough skin": {
            "mods":{"def": 10},
            "no_shop": True
            },
        },
    "legs": {
        "leather greaves":{
            "mods":{"def": 1},
            },
        }
    }

class Equipment(object):
    '''
    This class is for all equipment
    '''

    def __eq__(self, other):
        """
        Used to check if two Equipment objects are
        equal using the name as that should be unique
        for every equipment definition

        :other: The other equipment object
        :returns: boolean value, true for equal, false, for not

        """
        return self.name == other.name

    def __init__(self, name):
        self.name = name
        for key, values in armour.items():
            if name in values:
                self.equip_type = "armour"
                break
        else:
            self.equip_type = "weapons"
        def_dict = armour if 'r' in self.equip_type else weapons
        for key, values in def_dict.items():
            if name in values:
                self.type = key
                break
        else:
            raise KeyError("%s is not a %s" %(name, type(self).__name__))
        if 'n' in self.equip_type:
            self.hands_needed = def_dict[self.type][self.name][
                    "hands_needed"]
        self.mods = def_dict[self.type][self.name]["mods"]

    def describe_self(self, quantity = 0, other = ""):
        '''
        much like describe_ability in actions.py but specific
        for equipment
        '''

        heading = self.name.capitalize()
        body = "" if not quantity else "Quantity: %d\n" % quantity

        import main
        if self.mods:
            for stat,mod in self.mods.items():
                body += "%s: %d\n" %(
                        main.player_friendly_stats[
                            stat].capitalize(), mod)
        if "w" in self.equip_type:
            body += "Hands Needed: %d\n" %(self.hands_needed)
        body += other
        return main.create_info_board(heading, body)
