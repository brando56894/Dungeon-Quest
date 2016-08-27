#/usr/bin/python
#
#~battle.py

from random import random
from superRandom import superRandint
from charANPC import ANPC
from skills import skills
from copy import deepcopy

'''

atkDict = {
    * = tested via 1000 autoTests and 10 supervised test

    *"target": 0 for character-defined target,
                1 for character,
                2 for character allies,
                3 for character enemies,
                4 for atk-defined (i.e counter atk)
    *"baseAtk": percentage of strength used,
    *"baseAcc": percent accuracy of atk,
    *"atkStr": "string printed when attack is launched",
    *"spUsed": sp used for attack,
    *"mod": {"stat to be modified": modification,...},
    *"modString": "string to be reported upon mod",
    *"mpUsed": mp used for attack, 0 for physical attack,
    *"skipToFront": boolean True for skip False for no skip,
    *"waitForHit": {
        "recieveDmg": boolean True if dmg will be accepted False if dmg will not be accecpted,
        "recieveStr": "string that will be printed when hit and recieveDmg == False"
        "counterAtk":boolean True if counter atk False if not,
        "counterAtkStr": "string that will be printed upon counter strike"
    },
    *"waitForNextTurn": {
        "recieveDmg": boolean True if dmg will be accepted False if dmg will not be accecpted,
        "waitTurns": must be >= 1 how many turns will be skipped,
        "waitStr": "string reported everyone skipped turn",
        "afterWaitStr": "string reported after wait"
    },
    *"multiHit": {
        "numHits": 0 for random >0 for specific amount of turns,
        "repeatStr": "string to be reapeated after every hit"
    },
    "*targetLoseTurn": "string to appear when target loses turn",
    "*absorb": {
        "statBenfit": "stat that will benefit from absorption",
        "factor": percent of damage absorbed
    },
    #yet to be implemented
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

def cleanUp():
    #reset these dictionaries after each round
    global targetLoseTurn, waitForHit
    for charName in waitForHit:
        sendToScreen(charName + "'s attack failed.")
    waitForHit = {}
    targetLoseTurn = {}

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
        charAtkDicts[e] = (waitForNextTurn[e] if e in
                waitForNextTurn else everyone[e].AIAtk(
                    allies, enemies) if e == player
                else everyone[e].AIAtk(allies, enemies))

#decide play order
def decideOrder():
    global faction, order
    everyoneAlive = faction["allies"] + faction["enemies"]
    priority = filter(
            lambda x: charAtkDicts[x].get(
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
    targetName = atkDict.get("target")
    if character.checkIfDead():
        return 0
    sendToScreen(atkDict["atkStr"])
    if "waitForHit" in atkDict:
        waitForHit[charName] = atkDict
    elif "waitForNextTurn" in atkDict:
        if charName in waitForNextTurn:
            atk = waitForNextTurn[charName]
            waitDict = atk["waitForNextTurn"]
            turns = waitDict["waitTurns"]
            if turns:
                waitDict["waitTurns"] -= 1
            else:
                atk["atkStr"] = atk["waitForNextTurn"][
                        "afterWaitStr"]
                del atk["waitForNextTurn"]
                del waitForNextTurn[charName]
                attack(charName, atk)
        else:
            atk = atkDict
            atk["atkStr"] = atk["waitForNextTurn"][
                    "waitStr"]
            atk["waitForNextTurn"]["waitTurns"] -= 1
            waitForNextTurn[charName] = atk
    elif "multiHit" in atkDict:
        multDict = atkDict.get("multiHit")
        numHits = (multDict["numHits"] if multDict["numHits"]
                else superRandint(2,5))
        repeatStr = multDict["repeatStr"]
        for times in range(numHits):
            newStr = ''
            for word in repeatStr.split():
                newWord = word
                if "#" in word:
                    newWord = "#" + str(times + 1) + word[1:]
                newStr += newWord + ' '
            sendToScreen(newStr[:len(newStr) - 1])
            atkHandler(charName, targetName, atkDict)
    elif isinstance(targetName, int) and targetName != 4:
        for side in faction:
            if charName in faction[side]:
                team = faction[side]
            else:
                notTeam = faction[side]
        lis = ([charName] if targetName == 1 else
                team if targetName == 2 else
                notTeam if targetName == 3 else
                [])
        for char in lis:
            atkHandler(charName, char,
                    character.formatStringInDict(
                        deepcopy(atkDict), char))
    else:
        atkHandler(charName, targetName, atkDict)

def atkHandler(charName, targetName, atkDict):
    global waitForHit, waitForNextTurn
    if (everyone[targetName].checkIfDead() and
            "waitForNextTurn" not in atkDict):
        sendToScreen(charName + "'s attack failed.")
        return 0
    elif charName in targetLoseTurn:
        sendToScreen(targetLoseTurn[charName])
        return 0
    elif not checkAcc(charName, targetName, atkDict):
        sendToScreen(charName + " missed!")
    else:
        if targetName in waitForHit:
            targetAtk = waitForHit.pop(targetName)
            waitDict = targetAtk.pop("waitForHit")
            recieveDmg = waitDict["recieveDmg"]
            counterAtk = waitDict.get("counterAtk", False)
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
    modDict = atkDict.get("mod", {})
    lose = atkDict.get("targetLoseTurn", False)
    if lose:
        targetLoseTurn[targetName] = lose
    if modDict:
        modString = atkDict.get("modStr")
    else:
        modString = ''
    dmg = calcDmg(charName, targetName, atkDict)
    if dmg:
        modDict["hp"] = dmg
        sendToScreen("%s took %d damage!" %(targetName, -dmg))
    absorbDict = atkDict.get("absorb", False)
    if absorbDict:
        absorb(charName, dmg, absorbDict)
    target.statModifier(modDict)
    if modString:
        sendToScreen(modString)
    buryIfDead(targetName)

def absorb(charName, dmg, absorbDict):
    global everyone
    character = everyone[charName]
    stat = absorbDict["statBenefit"]
    factor = absorbDict["factor"]
    mod = int(round((factor / 100.0) * -dmg))
    character.statModifier({stat: mod})
    sendToScreen("%s gained %d %s!" %(charName, mod, stat))

def statusEffect():
    pass

def checkAcc(charName, targetName, atkDict):
    global everyone
    character = everyone[charName]
    target = everyone[targetName]
    baseAcc = atkDict.get("baseAcc")
    charAcc = character.stats["acc"]
    targetEva = target.stats["eva"]
    acc = (baseAcc/100.0) * (charAcc/targetEva)
    #make sure target is not on same team
    team = (faction["allies"] if charName in faction[
        "allies"] else faction["enemies"])
    sameTeam = True if targetName in team else False
    r = random()
    if not r < acc and not sameTeam:
        return False
    return True

def calcDmg(charName, targetName, atkDict):
    global everyone
    character = everyone[charName]
    target = everyone[targetName]
    magAtk = atkDict.get("mpUsed", 0)
    atk = character.stats["ma" if magAtk else "str"]
    defe = target.stats["md" if magAtk else "def"]
    lck = character.checkIfLucky()
    #defending character is given advantage
    atkDefRatio = ((atk * 1.0) / (defe * 2.0)) * lck
    baseAtk = (atkDict.get("baseAtk", 0) / 100.0) * atk
    if not baseAtk:
        return 0
    if lck == 2:
        sendToScreen('That\'s gonna leave a mark!')
    return int(round(-1 * (atkDefRatio + baseAtk)
        * atkDefRatio))

def buryIfDead(charName):
    global everyone, faction
    character = everyone[charName]
    if character.checkIfDead():
        sendToScreen("%s died." %(charName))
        for side in faction:
            if charName in faction[side]:
                faction[side].remove(charName)
                break

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
    count = 0
    while not checkIfEnd(player):
        count += 1
        #for sE in statusEffects:
        #    applyStatusEffects(sE, statusEffects[sE])
        collectAtks(player)
        decideOrder()
        sendToScreen('\nround ' + str(count))
        for c in order:
            attack(c, charAtkDicts[c])
            if checkIfEnd(player):
                break
        for e in everyone:
            everyone[e].SPMPRegen()
        cleanUp()

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
    MasaYume = ANPC({"name": "MasaYume",
        "equipment": {
            "head": "cap",
            "body": "rusty chainmail",
            "rightHand": "gauntlet",
            "leftHand": "dagger",
            "legs": "leather greaves"
            },
        "skills": {
            "fist": ["speed punch", "zen punch"],
            "dagger": ["backstab"]
            },
        })
    Brandon = ANPC({"name": "Brandon",
        "equipment": {
            "head": "cap",
            "body": "rusty chainmail",
            #this is two-handed so I only need to attach it to one hand
            "rightHand": "rifle",
            "legs": "leather greaves"
            },
        "skills": {
            "all": ["smokescreen", "trip"],
            "gun": ["focus shot"]
            },
        })
    typicalWarrior = ANPC({"name": "Kid Authur",
        "equipment": {
            "head": "cap",
            "body": "rusty chainmail",
            "rightHand": "sword",
            "leftHand": "wooden shield",
            "legs": "leather greaves"
            },
        "skills": {
            "all": ["warcry"],
            "blade": ["counter strike"],
            "shield": ["shield bash"]
            },
        })
    typicalArcher = ANPC({"name": "elf",
        "equipment": {
            "head": "cap",
            "body": "rusty chainmail",
            "rightHand": "bow",
            "legs": "leather greaves"
            },
        "skills": {
            "all": ["smokescreen"],
            "bow": ["arrow barrage", "spreadshot"]
            },
        })
    return battle(MasaYume, [Brandon],
            [typicalWarrior, typicalArcher])

if __name__ == "__main__":
    autoTest = 1000
    if autoTest:
        quiet = True
        wins = 0
        for x in range(autoTest):
            wins += test()
        print wins
    else:
        test()
