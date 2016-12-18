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
        #these items are specific to triggering events rather anywhere
        #or battle use so they only need a description
        "special": {
            "key": "I wonder what door this unlocks..."
            }
        }

class Item(object):
    '''
    class for all regualar items, not special items
    '''

    def __init__(self, name, dic = {}):
        if not dic:
            dic = items
        self.name = name
        for item_type, item_dic in dic.items():
            if name in item_dic:
                self.effect = item_dic[name]
                self.type = item_type
                if self.type != "special":
                    self.effect["NAME"] = name
                break
        else:
            raise KeyError("%s is not a %s" %(name, type(self).__name__))

    def use(self, char):
        mod = self.effect["mod"]
        mod_string = self.effect["mod_str"]
        char.stat_modifier(mod)
        print "%s %s" %(char.name, mod_string[5:])

    def describe_self(self, quantity = 0, other = ""):
        '''
        Used to describe skills and items
        '''
        heading = self.name.capitalize()

        #quantity
        body = "" if not quantity else "Quantity: %d\n" %quantity

        #type
        body += "Type: %s\n" %(self.type)

        if self.type != "special":
            #target
            target = self.effect.get("target", 0)
            if target:
                body += ("Target: " + ("all allies" if target == 2
                    else "all enemies" if target == 3 else "You")
                    + '\n')

            #base_atk, base_acc
            body += ("" if not self.effect.get("base_atk", 0) else
                    ("Strength: %d\n" %(self.effect["base_atk"])))
            body += ("" if not self.effect.get("base_acc", 0) else
                    ("Accuracy: %d\n" %(self.effect["base_acc"])))

            #sp_used, mp_used
            body += (("SP Used: %d\n" %(self.effect["sp_used"]))
                    if self.effect.get("sp_used", 0) else
                    ("MP Used: %d\n" %(self.effect["mp_used"])) if
                    self.effect.get("mp_used", 0) else "")

            #ability description
            body += "\n%s\n" %(self.effect["ability_descrip"])
        else:
            body += "\n"
            body += self.effect

        body += other

        import main
        return main.create_info_board(heading, body)
