#/usr/bin/python
#
#~battle.py

from random import random
from superRandom import superRandint
from charANPC import ANPC
from skills import *

'''

atkDict = {
    * = tested via 1000 autoTests and 10 supervised test

    "target": 0 for character-defined target,
                *1 for character,
                2 for character enemies,
                3 for character allies,
                4 for atk-defined (i.e counter atk)
    *"baseAtk": percentage of strength used,
    *"baseAcc": percent accuracy of atk,
    *"atkStr": "string printed when attack is launched",
    *"spUsed": sp used for attack,
    *"mod": {"stat to be modified": modification,...},
    *"modString": "string to be reported upon mod",
    *"mpUsed": mp used for attack, 0 for physical attack,
    "skipToFront": boolean True for skip False for no skip,
    "waitForHit": {
        "recieveDmg": boolean True if dmg will be accepted False if dmg will not be accecpted,
        "recieveStr": "string that will be printed when hit"
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

The following must be defined:
    baseAcc, atkStr

Only include in atkDict variables that are defined in atk or must be defined

'''
everyone = {}
faction = {}
order = []
targetLoseTurn = {}
waitForNextTurn = {}
waitForHit = {}
charAtkDicts = {}
statusEffects = {}
quiet = False

def sendToScreen(messege):
    '''
    this is in perperation for gui
    '''

    global quiet
    if not quiet:
        print messege

#apply any status effects
def applyStatusEffects(character, effect):
    pass

#collect attacks
def collectAtks(player):
    global everyone, charAtkDicts, faction, waitForNextTurn
    allies = faction["allies"]
    enemies = faction["enemies"]
    for e in everyone:
        if e not in waitForNextTurn:
            charAtkDicts[e] = (everyone[e].AIAtk(allies, enemies) if#askForAtk() if
                    e == player else everyone[e].AIAtk(
                        allies, enemies))

#decide play order
def decideOrder():
    global faction, order
    everyoneAlive = faction["allies"] + faction["enemies"]
    priority = filter(
            lambda x: charAtkDicts[x].pop(
                "skipToFront", False), everyoneAlive)
    order = filter(
            lambda x: True if x not in priority else False,
            everyoneAlive)
    for l in (order, priority):
        l.sort(key = lambda x: everyone[x].stats["spe"] *
                everyone[x].checkIfLucky())
    order = priority + order

#attack phase
def attack(charName, atkDict):
    global everyone, waitForHit, waitForNextTurn, faction
    character = everyone[charName]
    targetName = atkDict.pop("target")
    if character.checkIfDead():
        return 0
    if charName in targetLoseTurn:
        sendToScreen(targetLoseTurn[charName])
        return 0
    if isinstance(targetName, str):
        target = everyone[targetName]
    sendToScreen(atkDict.pop("atkStr"))
    if "waitForHit" in atkDict:
        waitForHit[charName] = atkDict
    elif "waitForNextTurn" in atkDict:
        waitForNextTurn[charName] = atkDict
    elif "multiHit" in atkDict:
        multDict = atkDict.pop("multiHit")
        numHits = multDict["numHits"]
        if not numHits:
            numHits = superRandint(2,5)
        repeatStr = multDict["repeatStr"]
        for times in range(numHits):
            sendToScreen(repeatStr)
            atkHandler(charName, targetName, atkDict)
    elif isinstance(targetName, int) and targetName != 4:
        if targetName == 1:
            lis = [charName]
        elif targetName == 2:
            lis = faction["allies"]
        elif targetName == 3:
            lis = faction["enemies"]
        for char in lis:
            targetName = char
            target = everyone[char]
            atkHandler(charName, targetName, atkDict)
    else:
        atkHandler(charName, targetName, atkDict)

def atkHandler(charName, targetName, atkDict):
    global waitForHit, waitForNextTurn
    if not checkAcc(charName, targetName, atkDict):
        sendToScreen(charName + " missed!")
    else:
        if targetName in waitForHit:
            targetAtk = waitForHit.pop(targetName)
            waitDict = targetAtk.pop("waitForHit")
            recieveDmg = waitDict["recieveDmg"]
            counterAtk = waitDict.pop("counterAtk", False)
            if recieveDmg:
                modAtk(charName, targetName, atkDict)
            else:
                recieveStr = waitDict["recieveStr"]
                sendToScreen(recieveStr)
            if counterAtk:
                targetAtk["atkStr"] = waitDict[
                        "counterStr"]
                targetAtk["target"] = charName
                attack(targetName, targetAtk)
        elif targetName in waitForNextTurn:
            recieveDmg = waitForNextTurn[targetName][
                    "waitForNextTurn"]["recieveDmg"]
            if recieveDmg:
                modAtk(charName, targetName, atkDict)
            else:
                sendToScreen(charName + " missed!")
        else:
            modAtk(charName, targetName, atkDict)

def modAtk(charName, targetName, atkDict):
    global everyone, targetLoseTurn
    target = everyone[targetName]
    modDict = atkDict.pop("mod", {})
    lose = atkDict.pop("targetLoseTurn", False)
    if lose:
        targetLoseTurn[targetName] = lose
    if modDict:
        modString = atkDict.pop("modStr")
    else:
        modString = ''
    dmg = calcDmg(charName, targetName, atkDict)
    if dmg:
        modDict["hp"] = dmg
        sendToScreen("%s took %d damage!" %(targetName, -dmg))
    target.statModifier(modDict)
    if modString:
        sendToScreen(modString)
    buryIfDead(targetName)

def absorb():
    pass

def statusEffect():
    pass

def checkAcc(charName, targetName, atkDict):
    global everyone
    character = everyone[charName]
    target = everyone[targetName]
    baseAcc = atkDict.pop("baseAcc")
    charAcc = character.stats["acc"]
    targetEva = target.stats["eva"]
    acc = (baseAcc/100.0) * (charAcc/targetEva)
    r = random()
    if not r < acc:
        return False
    return True

def calcDmg(charName, targetName, atkDict):
    global everyone
    character = everyone[charName]
    target = everyone[targetName]
    magAtk = atkDict.pop("mpUsed", 0)
    atk = character.stats["ma" if magAtk else "str"]
    defe = target.stats["md" if magAtk else "def"]
    lck = character.checkIfLucky()
    atkDefRatio = ((atk * 1.0) / (defe * 2.0)) * lck
    baseAtk = (atkDict.pop("baseAtk", 0) / 100.0) * atk
    if lck == 2:
        sendToScreen('That\'s gonna leave a mark!')
    return int(round(-1 * (atkDefRatio + baseAtk)
        * atkDefRatio))

def buryIfDead(charName):
    global everyone, faction
    character = everyone[charName]
    if character.checkIfDead():
        sendToScreen("%s died." %(charName))
        team = None
        for side in faction:
            if charName in faction[side]:
                team = faction[side]
                break
        team.remove(charName)

#check for end status
def checkIfEnd(player):
    enemies = faction["enemies"]
    if everyone[player].checkIfDead():
        return True
    elif not enemies:
        return True
    return False

def calcReward(player, allies, enemies):
    pass

def battle(player, allies, enemies):
    global everyone, charAtkDicts, statusEffects, faction, order
    allies.append(player)
    #throwing around strings is alot faster than
    #throwing around big objects
    for aE in allies + enemies:
        everyone[aE.name] = aE
    allies = [char.name for char in allies]
    enemies = [char.name for char in enemies]
    player = player.name
    faction["allies"] = allies
    faction["enemies"] = enemies
    #rewards = calcReward(player, allies, enemies)

    #battle flow
    while not checkIfEnd(player):
        #for sE in statusEffects:
        #    applyStatusEffects(sE, statusEffects[sE])
        collectAtks(player)
        decideOrder()
        for c in order:
            attack(c, charAtkDicts[c])
            if checkIfEnd(player):
                break
        for e in everyone:
            everyone[e].SPMPRegen()

    #checkIfLoseWin
    player = everyone[player]
    if player.checkIfDead():
        sendToScreen("You died.")
        return 0
    else:
        sendToScreen("You win!")
        return 1
        #win
        #rewards

def test():
    char1 = ANPC({"name": "MasaYume", "equipment": {}})
    char2 = ANPC({"name": "Brandon", "equipment": {}})
    char3 = ANPC({"name": "goon1", "equipment": {}})
    char4 = ANPC({"name": "goon2", "equipment": {}})
    char1.addSkill("staff", "magic blast")
    char2.addSkill("all", "warcry")
    return battle(char1, [char2], [char3, char4])

if __name__ == "__main__":
    autoTest = 0
    if autoTest:
        quiet = True
        wins = 0
        for x in range(autoTest):
            wins += test()
        print wins
    else:
        test()
