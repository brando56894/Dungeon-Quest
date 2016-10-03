#/usr/bin/python
#
#~items.py

#item definitions
#types anywhere, battle
items = {
        "anywhere":{
            "potion": {
                "target": 1,
                "mod": {"hp": 20},
                "atk_str": "name used a potion!",
                "mod_str": "name regained some health",
                "ability_descrip": "Replenishes some health.",
                #for now cost will be manually added to the item definition
                "cost": 20,
                },
            },
        "battle": {},
        }

#these items are specific to triggering events rather anywhere
#or battle use
special_items = [
    'key'
    ]

class Item(object):
    '''
    class for all regualar items, not special items
    '''

    def __init__(self, name):
        self.name = name
        for item_type, itemDic in items.items():
            if name in itemDic:
                self.effect = itemDic[name]

    def use(self, char):
        mod = self.effect["mod"]
        mod_string = self.effect["mod_str"]
        char.stat_modifier(mod)
        print "%s %s" %(char.name, mod_string[5:])
