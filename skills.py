#!/usr/bin/python
#
#~skills.py~

#skills definitions
'''

atk = {
    * = tested via 1000 auto_tests and 10 supervised test

    *"target": 0 for character-defined target,
                1 for character,
                2 for character allies,
                3 for character enemies,
                4 for atk-defined (i.e counter atk)
    *"base_atk": percentage of strength used,
    *"base_acc": percent accuracy of atk,
    *"atk_str": "string printed when attack is launched",
    *"sp_used": sp used for attack,
    *"mod": {"stat to be modified": modification,...},
    *"mod_string": "string to be reported upon mod",
    *"mp_used": mp used for attack, 0 for physical attack,
    *"skip_to_front": boolean True for skip False for no skip,
    *"wait_for_hit": {
        "recieve_dmg": boolean True if dmg will be accepted False if dmg will not be accecpted,
        "recieve_str": "string that will be printed when hit and recieve_dmg == False"
        "counter_atk":boolean True if counter atk False if not,
        "counter_atk_str": "string that will be printed upon counter strike"
    },
    *"wait_for_next_turn": {
        "recieve_dmg": boolean True if dmg will be accepted False if dmg will not be accecpted,
        "wait_turns": must be >= 1 how many turns will be skipped,
        "wait_str": "string reported everyone skipped turn",
        "after_wait_str": "string reported after wait"
    },
    *"multi_hit": {
        "num_hits": 0 for random >0 for specific amount of turns,
        "repeat_str": "string to be reapeated after every hit"
    },
    "*target_lose_turn": "string to appear when target loses turn",
    "*absorb": {
        "stat_benfit": "stat that will benefit from absorption",
        "factor": percent of damage absorbed
    },
    #yet to be implemented
    "status_effect": {
        "type": "type of status effect",
        "severity": 1 for normal
                    2 for mildly sever
                    3 for very sever
    }
}

The default for everything except the below is 0
The following must be defined:
    atk_str

Only include in atkDict variables that are defined in atk or must be defined

'''
skills = {
    "all": {
        "smokescreen": {
            "base_acc": 90,
            "atk_str": "name used smokescreen!",
            "mod": {"acc": .7},
            "mod_str": "target_name's accuracy lowered.",
            "sp_used": 2
            },
        "warcry": {
            "target": 1,
            "base_acc": 95,
            "atk_str": "name used warcry!",
            "mod": {"str": 1.5, "def": .75},
            "mod_str": "name's strength rose and defense lowered!",
            "sp_used": 2
            },
        "trip": {
            "base_atk": 10,
            "base_acc": 100,
            "atk_str": "name tripped target_name!",
            "target_lose_turn": ("target_name is having a hard"
                " time getting up!"),
            "sp_used": 1
            }
        },
    "blade": {
        "parry": {
            "target": 4,
            "base_acc": 100,
            "atk_str": "name used parry!",
            "wait_for_hit": {
                "recieve_dmg": 0,
                "recieve_str": "name parried the attack!",
                },
            "sp_used": 1
            },
        "counter strike": {
            "target": 4,
            "base_atk": 70,
            "base_acc": 100,
            "atk_str": "name used counter strike!",
            "wait_for_hit": {
                "recieve_dmg": 0,
                "recieve_str": "name blocked the attack!",
                "counter_atk": 1,
                "counter_atk_str": "name unleashed a counter attack!"
                },
            "sp_used": 5
            },
        },
    "shield": {
        "shield bash": {
            "base_atk": 85,
            "base_acc": 90,
            "atk_str": "name used sheild bash!",
            "mod": {"str": .9},
            "mod_str": "target_name's strength lowered.",
            "sp_used": 3
            },
        },
    "staff": {
        "magic blast": {
            "base_atk": 75,
            "base_acc": 90,
            "atk_str": "name used magic blast!",
            "mp_used": 3,
            },
        "cure": {
            "target": 1,
            "base_acc": 100,
            "atk_str": "name used cure!",
            "mod": {"hp": 5},
            "mod_str": "name regained some health!",
            "mp_used": 2
            },
        "cure allies": {
            "target": 2,
            "base_acc": 100,
            "atk_str": "name used cure allies!",
            "mod": {"hp": 10},
            "mod_str": "target_name regained some health!",
            "mp_used": 8
            },
        "fireball": {
            "base_atk": 90,
            "base_acc": 90,
            "atk_str": "name used fireball!",
            "mp_used": 8,
            },
        },
    "dagger": {
        "backstab": {
            "base_atk": 85,
            "base_acc": 90,
            "atk_str": "name used backstab!",
            "mod": {"def": .7},
            "mod_str": "target_name's defense lowered.",
            "sp_used": 3
            },
        "vampire strike": {
            "base_atk": 75,
            "base_acc": 80,
            "atk_str": "name used vapire strike!",
            "absorb": {
                "stat_benefit": "hp",
                "factor": 50
                },
            "sp_used": 5
            }
        },
    "gun": {
            "focus shot": {
                "base_atk": 100,
                "base_acc": 100,
                "atk_str": "name is calming his mind...",
                "wait_for_next_turn": {
                    "recieve_dmg": 1,
                    "wait_turns": 2,
                    "wait_str": "name is focusing...",
                    "after_wait_str": "name used focus shot!"
                    },
                "sp_used": 10,
                }
        },
    "bow":{
            "arrow barrage": {
                "base_atk": 40,
                "base_acc": 95,
                "atk_str": "name used arrow barrage!",
                "multi_hit": {
                    "num_hits": 0,
                    "repeat_str": "Here comes arrow #!"
                    },
                "sp_used": 4,
                },
            "spreadshot": {
                "target": 3,
                "base_atk": 60,
                "base_acc": 90,
                "atk_str": "name used spread shot!",
                "sp_used": 4
                }
        },
    "fist":{
            "speed punch": {
                "base_atk": 50,
                "base_acc": 95,
                "atk_str": "name used speed punch!",
                "skip_to_front": True,
                "sp_used": 2
                },
            "zen punch": {
                "base_atk": 100,
                "base_acc": 100,
                "atk_str": "name began meditating...",
                "wait_for_next_turn": {
                    "recieve_dmg": 1,
                    "wait_turns": 2,
                    "wait_str": "name is meditating...",
                    "after_wait_str": "name used zen punch!"
                    },
                "sp_used": 10,
                }
        },
    }
