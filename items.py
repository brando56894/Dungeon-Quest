#/usr/bin/python
#
#~items.py

#item definitions
#types anywhere, battle, special
items = {
        "anywhere":{
            "potion": {
                "target": 1,
                "mod": {"hp": 20},
                "atk_string": "name used a potion!",
                "mod_string": "name regained some health",
                "ability_descrip": "Replenishes some health.",
                #for now cost will be manually added to the item definition
                "cost": 20,
                },
            },
        "battle": {},
        }

special_items = [
    'key'
    ]
class Item(object):

    def __init__(self, name):
        self.name = name
        for item_type, itemDic in items.items():
            if name in itemDic:
                self.effect = itemDic[name]
        pass

    def use(self, char):
        mod = self.effect["mod"]
        mod_string = self.effect["mod_string"]
        char.statModifier(mod)
        print char.name + mod_string[5:]
