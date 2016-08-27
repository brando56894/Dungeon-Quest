#!/usr/bin/python
#
#~skills.py~

#skills definitions
skills = {
    "all": {
        "smokescreen": {
            "baseAcc": 90,
            "atkStr": "name used smokescreen!",
            "mod": {"acc": .7},
            "modStr": "targetName's accuracy lowered.",
            "spUsed": 2
            },
        "warcry": {
            "target": 1,
            "baseAcc": 95,
            "atkStr": "name used warcry!",
            "mod": {"str": 1.5, "def": .75},
            "modStr": "name's strength rose and defense lowered!",
            "spUsed": 2
            },
        "trip": {
            "baseAtk": 10,
            "baseAcc": 100,
            "atkStr": "name tripped targetName!",
            "targetLoseTurn": ("targetName is having a hard"
                " time getting up!"),
            "spUsed": 1
            }
        },
    "blade": {
        "parry": {
            "target": 4,
            "baseAcc": 100,
            "atkStr": "name used parry!",
            "waitForHit": {
                "recieveDmg": 0,
                "recieveStr": "name parried the attack!",
                },
            "spUsed": 1
            },
        "counter strike": {
            "target": 4,
            "baseAtk": 70,
            "baseAcc": 100,
            "atkStr": "name used counter strike!",
            "waitForHit": {
                "recieveDmg": 0,
                "recieveStr": "name blocked the attack!",
                "counterAtk": 1,
                "counterStr": "name unleashed a counter attack!"
                },
            "spUsed": 5
            },
        },
    "shield": {
        "shield bash": {
            "baseAtk": 85,
            "baseAcc": 90,
            "atkStr": "name used sheild bash!",
            "mod": {"str": .9},
            "modStr": "targetName's strength lowered.",
            "spUsed": 3
            },
        },
    "staff": {
        "magic blast": {
            "baseAtk": 75,
            "baseAcc": 90,
            "atkStr": "name used magic blast!",
            "mpUsed": 3,
            },
        "cure": {
            "target": 1,
            "baseAcc": 100,
            "atkStr": "name used cure!",
            "mod": {"hp": 5},
            "modStr": "name regained some health!",
            "mpUsed": 2
            },
        "cure allies": {
            "target": 2,
            "baseAcc": 100,
            "atkStr": "name used cure allies!",
            "mod": {"hp": 5},
            "modStr": "targetName regained some health!",
            "mpUsed": 8
            },
        },
    "dagger": {
        "backstab": {
            "baseAtk": 85,
            "baseAcc": 90,
            "atkStr": "name used backstab!",
            "mod": {"def": .7},
            "modStr": "targetName's defense lowered.",
            "spUsed": 3
            },
        "vampire strike": {
            "baseAtk": 75,
            "baseAcc": 80,
            "atkStr": "name used vapire strike!",
            "absorb": {
                "statBenefit": "hp",
                "factor": 50
                },
            "spUsed": 5
            }
        },
    "gun": {
            "focus shot": {
                "baseAtk": 100,
                "baseAcc": 100,
                "atkStr": "name is calming his mind...",
                "waitForNextTurn": {
                    "recieveDmg": 1,
                    "waitTurns": 2,
                    "waitStr": "name is focusing...",
                    "afterWaitStr": "name used focus shot!"
                    },
                "spUsed": 10,
                }
        },
    "bow":{
            "arrow barrage": {
                "baseAtk": 40,
                "baseAcc": 95,
                "atkStr": "name used arrow barrage!",
                "multiHit": {
                    "numHits": 0,
                    "repeatStr": "Here comes arrow #!"
                    },
                "spUsed": 4,
                },
            "spreadshot": {
                "target": 3,
                "baseAtk": 60,
                "baseAcc": 90,
                "atkStr": "name used spread shot!",
                "spUsed": 4
                }
        },
    "fist":{
            "speed punch": {
                "baseAtk": 50,
                "baseAcc": 95,
                "atkStr": "name used speed punch!",
                "skipToFront": True,
                "spUsed": 2
                },
            "zen punch": {
                "baseAtk": 100,
                "baseAcc": 100,
                "atkStr": "name began meditating...",
                "waitForNextTurn": {
                    "recieveDmg": 1,
                    "waitTurns": 2,
                    "waitStr": "name is meditating...",
                    "afterWaitStr": "name used zen punch!"
                    },
                "spUsed": 10,
                }
        },
    }
