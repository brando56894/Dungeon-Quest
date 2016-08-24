#/usr/bin/python
#
#~battle.py

def battle(player, allies, enemies):
    allies.append(player)
    everyone = allies + enemies
    order = []
    charAtkDicts = {}
    statusEffects = {}

    #Lets start simple
    #apply any status effects
    #def applyStatusEffects(character, effect):
    #    pass
    #decide play order
    def decideOrder():
        pass
    #attack phase
    def attack(character, atkDict):
        pass
    #check for end status
    def checkIfEnd():
        pass

    while not checkIfEnd():
        #for sE in statusEffects:
        #    applyStatusEffects(sE, statusEffects[sE])
        decideOrder()
        for c in order:
            attack(c, charAtkDicts[c])
            if checkIfEnd():
                break

    if not player.stats["hp"]:
        #lose
        pass
    else:
        #win
        #rewards
        pass
