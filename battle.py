#/usr/bin/python
#
#~battle.py
'''

    atkDict = {
        "target": 0 for character-defined target,
                  1 for character,
                  2 for character enemies,
                  3 for character allies
        "baseAtk": percentage of strength used,
        "baseAcc": percent accuracy of atk,
        "atkStr": "string printed when attack is launched",
        "spUsed": sp used for attack,
        "mod": {"stat to be modified": modification,...},
        "modString": "string to be reported upon mod",
        "mpUsed": mp used for attack, 0 for physical attack,
        "skipToFront": boolean True for skip False for no skip,
        "waitForHit": {
            "recieveDmg": boolean True if dmg will be accepted False if dmg will not be accecpted,
            "counterAtk":boolean True if counter atk False if not,
            "counterAtkStr": "string that will be printed upon counter strike"
        },
        "waitForNextTurn": {
            "recieveDmg": boolean True if dmg will be accepted False if dmg will not be accecpted,
            "waitTurns": must be >= 1 how many turns will be skipped,
            "waitStr": "string reported everyone skipped turn",
            "afterWaitStr": "string reported after wait"
        },
        "multiHit": {
            "numHits": 0 for random >0 for specific amount of turns,
            "repeatStr": "string to be reapeated after every hit"
        },
        "targetLoseTurn": "string to appear when target loses turn",
        "absorb": {
            "statBenfit": "stat that will benefit from absorption",
            "factor": percent of damage absorbed
        },
        "statusEffect": {
            "type": "type of status effect",
            "severity": 1 for normal
                        2 for mildly sever
                        3 for very sever
        }
    }

    The default for everything is 0 except the following:
        baseAcc, atkStr

    Only include in atkDict variables that have no default, or are defined in atk

    '''
everyone = {}
order = []
waitForNextTurn = {}
waitForHit = {}
charAtkDicts = {}
statusEffects = {}

#apply any status effects
#def applyStatusEffects(character, effect):
#    pass

#decide play order
def decideOrder():
    global everyone, order
    priority = filter(
            lambda x: charAtkDicts[everyone[x]].pop(
                "skipToFront", False), everyone)
    order = filter(
            lambda x: True if x not in priority else False,
            everyone)
    for l in (order, priority):
        l.sort(key = lambda x: everyone[x].stats["spe"] *
                everyone[x].checkIfLucky())
    order = priority + order
    print order

#attack phase
def attack(character, atkDict):
    #character is string
    #use everyone to get object

    def modAtk(target, atkDict):

        def absorb():
            pass

        def statusEffect():
            pass
    
        pass

    def waitForHit():
        pass

    def waitForNextTurn():
        pass

    def multiHit():
        pass

    def multiTarget():
        pass

    if atkDict.pop("waitForHit", False):
        waitForHit[character] = atkDict
    elif atkDict.pop("waitForNextTurn", False):
        waitForNextTurn[character] = atkDict
    elif atkDict.pop("multiHit", False):
        pass
    elif atkDict.pop("multiTarget", False):
        pass
    else:
        pass
    pass

#check for end status
def checkIfEnd(player, enemies):
    if not everyone[player].stats["hp"]:
        return True
    elif not enemies:
        return True
    return False

def calcReward(player, allies, enemies):
    pass

def battle(player, allies, enemies):
    global everyone, charAtkDicts, statusEffects
    allies.append(player)
    #rewards = calcReward(player, allies, enemies)

    #throwing around strings is alot faster than
    #throwing around big objects
    for aE in allies + enemies:
        everyone[aE.name] = aE
    for aE in (allies, enemies):
        aE = [char.name for char in aE]
    player = player.name

    #collect attacks
    for e in everyone:
        charAtkDicts[e] = (everyone[e].askForAtk() if
                e == player elif everyone[e] not in
                waitForNextTurn everyone[e].AIAtk())

    #battle flow
    while not checkIfEnd(enemies):
        #for sE in statusEffects:
        #    applyStatusEffects(sE, statusEffects[sE])
        decideOrder()
        for c in order:
            attack(c, charAtkDicts[c])
            if checkIfEnd(enemies):
                break

    #checkIfLoseWin
    player = everyone[player]
    if not player.stats["hp"]:
        print("You died.")
        return 0
    else:
        #win
        #rewards
        pass
