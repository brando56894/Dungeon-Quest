#!/usr/bin/python
#
#~skills.py~

#skills definitions
skills = {
    "any": {
        'smokescreen': {
            'baseAcc': 90,
            'atkString': 'name used smokescreen!',
            'mod': {'acc': .7},
            'modString': "targetName's accuracy lowered.",
            'sp': 2
            },
        'warcry': {
            'target': 'name',
            'baseAcc': 95,
            'atkString': 'name used warcry!',
            'mod': {'atk': 1.5, 'def': .75},
            'modString': "name's attack rose and defense lowered!",
            'sp': 2
            },
        },
    "blade": {
        'parry': {
            'target': 'name',
            'baseAcc': 100,
            'atkString': 'name used parry!',
            'waitForHit': [1, 0, 0, 'name parried the attack!'],
            'sp': 1
            },
        },
    "sheild": {
        'sheild bash': {
            'baseAtk': 85,
            'baseAcc': 90,
            'atkString': 'name used sheild bash!',
            'mod': {'atk': .9},
            'modString': "targetName's attack lowered.",
            'sp': 3
            },
        },
    "staff": {
        'magic blast': {
            'baseAtk': 75,
            'baseAcc': 90,
            'atkString': 'name used magic blast!',
            'magAtk': True,
            'sp': 3
            },
        'cure': {
            'target': 'name',
            'baseAcc': 100,
            'atkString': 'name used cure!',
            'mod': {'hp': 5},
            'modString': 'name regained some health!',
            'sp': 2
            },
        },
    "dagger" {
        'backstab': {
            'baseAtk': 85,
            'baseAcc': 90,
            'atkString': 'name used backstab!',
            'mod': {'def': .7},
            'modString': "targetName's defense lowered.",
            'sp': 3
            },
        },
    "gun": {
        },
    "bow":{
        },
    "fist":{
        },
    }
