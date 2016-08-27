#!/usr/bin/python
#
#~skills.py~

#skills definitions
skills = {
    "all": {
        'smokescreen': {
            'baseAcc': 90,
            'atkStr': 'name used smokescreen!',
            'mod': {'acc': .7},
            'modStr': "targetName's accuracy lowered.",
            'spUsed': 2
            },
        'warcry': {
            'target': 1,
            'baseAcc': 95,
            'atkStr': 'name used warcry!',
            'mod': {'str': 1.5, 'def': .75},
            'modStr': "name's strength rose and defense lowered!",
            'spUsed': 2
            },
        "trip": {
            "baseAtk": 10,
            "baseAcc": 100,
            "atkStr": "name used trip!",
            "targetLoseTurn": "targetName tripped!",
            "spUsed": 1
            }
        },
    "blade": {
        'parry': {
            'target': 4,
            'baseAcc': 100,
            'atkStr': 'name used parry!',
            'waitForHit': {
                "recieveDmg": 0,
                "recieveStr": "name parried the attack!",
                },
            'spUsed': 1
            },
        },
    "sheild": {
        'sheild bash': {
            'baseAtk': 85,
            'baseAcc': 90,
            'atkStr': 'name used sheild bash!',
            'mod': {'str': .9},
            'modStr': "targetName's strength lowered.",
            'spUsed': 3
            },
        },
    "staff": {
        'magic blast': {
            'baseAtk': 75,
            'baseAcc': 90,
            'atkStr': 'name used magic blast!',
            'mpUsed': 3,
            },
        'cure': {
            'target': 1,
            'baseAcc': 100,
            'atkStr': 'name used cure!',
            'mod': {'hp': 5},
            'modStr': 'name regained some health!',
            'spUsed': 2
            },
        },
    "dagger": {
        'backstab': {
            'baseAtk': 85,
            'baseAcc': 90,
            'atkStr': 'name used backstab!',
            'mod': {'def': .7},
            'modStr': "targetName's defense lowered.",
            'spUsed': 3
            },
        },
    "gun": {
            "focus shot": {
                "baseAtk": 90,
                "baseAcc": 100,
                "atkStr": "name is calming their mind...",
                "waitForNextTurn": {
                    "recieveDmg": 1,
                    "waitTurns": 1,
                    "waitStr": "name is focusing...",
                    "afterWaitStr": "name used focus shot!"
                    },
                "spUsed": 6,
                }
        },
    "bow":{
            "arrow barrage": {
                "baseAtk": 40,
                "baseAcc": 95,
                "atkStr": "name used arrow barrage!",
                "multiHit": {
                    "numHits": 0,
                    "repeatStr": "Bam!" #this is probably unneccessary
                    },
                "spUsed": 4,
                }
        },
    "fist":{
            "speed punch": {
                "baseAtk": 50,
                "baseAcc": 95,
                "atkStr": "name used suckerpunch!",
                "skipToFront": True,
                "spUsed": 2
                },
        },
    }
