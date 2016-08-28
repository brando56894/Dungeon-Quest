#/usr/bin/python
#
#~items.py

#item definitions
#types anywhere, battle, special
items = {
        "anywhere":{
            "potion": {
                "effect": {
                    "target": 1,
                    "mod": {"hp": 20},
                    "atk_string": "name used a potion!",
                    "mod_string": "name regained some health"
                    }
                },
            },
        "battle": {},
        "special": [
            'key'
            ]
        }
