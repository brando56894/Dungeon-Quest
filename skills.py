#!/usr/bin/python
#
#~skills.py~

#algorithm for deciding the cost of skills
calc_cost = lambda atk: (atk["sp_used"] if atk.get("sp_used", 0) else atk["mp_used"]) * 10 #pretty basic for now

#skills definitions
'''

atk = {
    * = tested via 1000 auto_tests and 10 supervised test and 1 participated test

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
    *"target_lose_turn": "string to appear when target loses turn",
    *"absorb": {
        "stat_benfit": "stat that will benefit from absorption",
        "factor": percent of damage absorbed
    },
    "ability_descrip": ("string describing the abilities"
                        "of the skill (i.e stat modifications,"
                        "multi hit capability, etc. Look at"
                        "other skills for examples")
                        ),
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
    atk_str, ability_descrip

Only include in atkDict variables that are defined in atk or must be defined

Shortcuts for all strings:
    target_name = name of next target
    name = character name
    atk_name = name of atk #yet to be implemented
'''
#TODO: make strings more interesting to read
skills = {
    "all": {
        "smokescreen": {
            "base_acc": 90,
            "atk_str": "name used smokescreen!",
            "mod": {"acc": .7},
            "mod_str": "target_name's accuracy lowered.",
            "sp_used": 2,
            "ability_descrip":("A black mist will surround "
                "the enemy\nthus reducing their vision by 70%.")
            },
        "warcry": {
            "target": 1,
            "base_acc": 95,
            "atk_str": "name used warcry!",
            "mod": {"str": 1.5, "def": .75},
            "mod_str": "name's strength rose and defense lowered!",
            "sp_used": 2,
            "ability_descrip":("Shouting this bloodcurdling "
                "cry will\nincrease strength but decrease defense.")
            },
        "trip": {
            "base_atk": 10,
            "base_acc": 100,
            "atk_str": "name tripped target_name!",
            "target_lose_turn": ("target_name is having a hard"
                " time getting up!"),
            "sp_used": 1,
            "ability_descrip":("This attack may be weak, "
                "but the enemy\nwill not be quick to get "
                "up afterwards.")
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
            "sp_used": 1,
            "ability_descrip":"Parry away incoming attacks."
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
            "sp_used": 5,
            "ability_descrip":("Incoming attacks will "
                "not only be parried\naway but a counter "
                "attack will be launched.")
            },
        },
    "shield": {
        "shield bash": {
            "base_atk": 85,
            "base_acc": 90,
            "atk_str": "name used sheild bash!",
            "mod": {"str": .9},
            "mod_str": "target_name's strength lowered.",
            "sp_used": 3,
            "ability_descrip":("The enemy will soon learn "
                "that the best offence\nis the best defence"
                ", but it will cost them their\nstrength.")
            },
        },
    "staff": {
        "magic blast": {
            "base_atk": 75,
            "base_acc": 90,
            "atk_str": "name used magic blast!",
            "mp_used": 3,
            "ability_descrip":("Blast of magic that packs a "
                "punch.")
            },
        "cure": {
            "target": 1,
            "base_acc": 100,
            "atk_str": "name used cure!",
            "mod": {"hp": 5},
            "mod_str": "name regained some health!",
            "mp_used": 2,
            "ability_descrip":("Spell that heals wounds a "
                "little bit.")
            },
        "cure allies": {
            "target": 2,
            "base_acc": 100,
            "atk_str": "name used cure allies!",
            "mod": {"hp": 10},
            "mod_str": "target_name regained some health!",
            "mp_used": 8,
            "ability_descrip":("Spell that heals ally "
                "health a little bit.")
            },
        "fireball": {
            "base_atk": 90,
            "base_acc": 90,
            "atk_str": "name used fireball!",
            "mp_used": 8,
            "ability_descrip":("Ball of fire that engulfs "
                "anything in its path.")
            },
        },
    "dagger": {
        "backstab": {
            "base_atk": 85,
            "base_acc": 90,
            "atk_str": "name used backstab!",
            "mod": {"def": .7},
            "mod_str": "target_name's defense lowered.",
            "sp_used": 3,
            "ability_descrip":("A stab in the back that "
                "will make it\neasier to attack from the "
                "front.")
            },
        "vampire strike": {
            "base_atk": 75,
            "base_acc": 80,
            "atk_str": "name used vampire strike!",
            "absorb": {
                "stat_benefit": "hp",
                "factor": 50
                },
            "mp_used": 5,
            "ability_descrip":("With every strike, what has "
                "been sowed\nin damage will be reaped in health.")
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
                "ability_descrip":("Only the best sniper "
                    "knows that when one calms\nand focuses "
                    "their mind for a while the best shot\n"
                    "possible is made clear.")
                }
        },
    "bow":{
            "arrow barrage": {
                "base_atk": 40,
                "base_acc": 90,
                "atk_str": "name used arrow barrage!",
                "multi_hit": {
                    "num_hits": 0,
                    "repeat_str": "Here comes arrow #!"
                    },
                "sp_used": 4,
                "ability_descrip":("The enemy better be "
                    "hungry because,\nhere comes a arrow "
                    "buffet.")
                },
            "spreadshot": {
                "target": 3,
                "base_atk": 60,
                "base_acc": 90,
                "atk_str": "name used spread shot!",
                "sp_used": 4,
                "ability_descrip":("Why attack one enemy at "
                    "a time when\nyou can take them all on.")
                }
        },
    "fist":{
            "speed punch": {
                "base_atk": 50,
                "base_acc": 95,
                "atk_str": "name used speed punch!",
                "skip_to_front": True,
                "sp_used": 2,
                "ability_descrip":("The early punch takes "
                    "the enemies head.")
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
                "ability_descrip":("A powerfull punch that is "
                    "the result\nof constant meditation.")
                }
        },
    }

