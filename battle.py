#/usr/bin/python
#
#~battle.py

from random import random
from superRandom import super_randint, super_choice
from skills import skills
from copy import deepcopy
import main

#testing purposes
import anpc
import player

#define global variables
everyone = {}
faction = {}
order = []
target_lose_turn = {}
wait_for_next_turn = {}
wait_for_hit = {}
char_atk_dicts = {}
status_effects = {}
player_stats_copy = {} #allows some stats to go back to normal
quiet = False
run_ability = True

def send_to_screen(messege):
    '''
    prints message if not quiet

    This will be a lot more complicated when gui
    is implemented so I thought I would get it
    started
    '''

    global quiet
    if not quiet:
        print messege

def battle(player, allies = [], enemies = [], can_run = True):
    '''
    This is the battle loop
    '''

    global everyone, char_atk_dicts, status_effects
    global faction, order, run_ability, player_stat_copy
    player_stat_copy = deepcopy(player.stats)
    #throwing around strings is alot faster than
    #throwing around big objects
    allies.append(player)
    for aE in allies + enemies:
        everyone[aE.name] = aE
    allies = [char.name for char in allies]
    enemies = [char.name for char in enemies]
    player = player.name
    faction["allies"] = allies
    faction["enemies"] = enemies
    run_ability = can_run
    rewards = calc_reward(player, enemies)

    count = 0
    ran = False
    while not check_if_end(player):
        count += 1
        #for sE in status_effects:
        #    apply_status_effects(sE, status_effects[sE])
        if collect_atks(player):
            ran = True
            break
        main.clearscreen(everyone[player])
        decide_order(player)
        send_to_screen('round ' + str(count))
        if char_atk_dicts[player] == "run":
            send_to_screen("You couldn't run away!")
        for c in order:
            attack(c, char_atk_dicts[c])
            if check_if_end(player):
                break
        for e in everyone:
            everyone[e].SPMP_regen()
        clean_up()
        main.confirm()

    player = everyone[player]
    main.clearscreen(player)
    if player.check_if_dead():
        send_to_screen("You died.")
        return 0
    elif ran:
        send_to_screen("You ran.")
        #resets some stats to normal
        #hp stays the same
        for stat, value in player_stat_copy.items():
            if "hp" not in stat:
                player.stats[stat] = value
        player.stats["run_away"] += 1
        return 0
    else:
        send_to_screen("You win!")
        #resets some stats to normal
        #hp stays the same
        for stat, value in player_stat_copy.items():
            if "hp" not in stat:
                player.stats[stat] = value
        #give items
        for item, quantity in rewards.pop("items").items():
            send_to_screen("\nYou recieved %d %s!" %(quantity, item))
            player.edit_inv(item, quantity)
        #give stats
        for stat, mod in rewards.items():
            send_to_screen("\nYou recieved %d %s!" %(mod, stat))
            player.stat_modifier({stat:mod})
        return 1

def calc_reward(player, enemies):
    #inventory
    inv = {}
    for char in enemies:
        inventory = everyone[char].inventory
        for item, quantity in inventory.items():
            inv[item] = (inv[item] + quantity
                    if item in inv else quantity)
    items = {}
    for item, quanitity in inv.items():
        if super_choice([1,0]):
            items[item] = (super_randint(0,quantity)
                    * everyone[player].check_if_lucky())

    reward_dict = {"items": items}
    #gold, exp
    for stat in ("gold", "exp"):
        total = reduce((lambda x,t: x+y),
                [everyone[char].stats[stat]
                    for char in enemies])
        stat_value = (total * everyone[player].check_if_lucky()
                / len(enemies))
        reward_dict[stat] = stat_value
    return reward_dict

def clean_up():
    '''
    reset some variables after each round
    '''

    global target_lose_turn, wait_for_hit
    for char_name in wait_for_hit:
        send_to_screen(char_name + "'s attack failed.")
    wait_for_hit = {}
    target_lose_turn = {}

#apply any status effects
#def apply_status_effects(character, effect):
#    pass

def collect_atks(player):
    '''
    collects atks from all alive characters
    '''

    global everyone, char_atk_dicts, faction, wait_for_next_turn
    allies = faction["allies"]
    enemies = faction["enemies"]
    for e in everyone:
        char_atk_dicts[e] = (wait_for_next_turn[e] if e in
                wait_for_next_turn else everyone[e].battle_prompt(
                    allies, enemies) if e == player
                else everyone[e].AI_atk(allies, enemies))
    if run_check(player):
        return True

def run_check(player):
    '''
    checks if the player's run attempt is successfull
    by looking at team averages in speed and luck
    '''

    global everyone, faction, run_ability
    if not run_ability:
        sendToScreen("You can't run from this fight!")
        return False
    #I can assume player is on allies
    allies_len = len(faction["allies"])
    enemy_len = len(faction["enemies"])
    faction_avg = {}
    if char_atk_dicts[player] == "run":
        for team in faction:
            teamList = faction[team]
            team_lck = reduce(lambda x,y:x+y,
                    [everyone[char].check_if_lucky()
                        for char in teamList])
            team_spe = reduce(lambda x,y:x+y,
                    [everyone[char].stats["spe"]
                        for char in teamList])
            team_len = len(faction[team])
            faction_avg[team] = ((team_lck * team_spe) *
                    (team_len ** 2))
        if faction_avg["allies"] >= faction_avg["enemies"]:
            return True



def decide_order(player):
    '''
    decides the order
    '''

    global faction, order, char_atk_dicts
    everyone_alive = faction["allies"] + faction["enemies"]
    if char_atk_dicts[player] == "run":
        everyone_alive.remove(player)
    priority = filter(
            lambda x: char_atk_dicts[x].get(
                "skip_to_front", False), everyone_alive)
    order = filter(
            lambda x: True if x not in priority else False,
            everyone_alive)
    for l in (order, priority):
        l.sort(key = lambda x: everyone[x].stats["spe"] *
                everyone[x].check_if_lucky())
    order = priority + order

def attack(char_name, atk_dict):
    '''
    This can be seen as the pre_atk_handler

    Takes care of anything in need of special attention before
    sending it off to atk_handler
    '''

    global everyone, wait_for_hit, wait_for_next_turn, faction
    character = everyone[char_name]
    target_name = atk_dict.get("target")
    if character.check_if_dead() or atk_dict == "run":
        #if player tries to run but fails they lose turn
        return 0
    send_to_screen(atk_dict["atk_str"])
    if "wait_for_hit" in atk_dict:
        wait_for_hit[char_name] = atk_dict
    elif "wait_for_next_turn" in atk_dict:
        if char_name in wait_for_next_turn:
            atk = wait_for_next_turn[char_name]
            wait_dict = atk["wait_for_next_turn"]
            turns = wait_dict["wait_turns"]
            if turns:
                wait_dict["wait_turns"] -= 1
            else:
                atk["atk_str"] = atk["wait_for_next_turn"][
                        "after_wait_str"]
                del atk["wait_for_next_turn"]
                del wait_for_next_turn[char_name]
                attack(char_name, atk)
        else:
            atk = atk_dict
            atk["atk_str"] = atk["wait_for_next_turn"][
                    "wait_str"]
            atk["wait_for_next_turn"]["wait_turns"] -= 1
            wait_for_next_turn[char_name] = atk
    elif "multi_hit" in atk_dict:
        mult_dict = atk_dict.get("multi_hit")
        num_hits = (mult_dict["num_hits"] if mult_dict["num_hits"]
                else super_randint(2,5))
        repeat_str = mult_dict["repeat_str"]
        for times in range(num_hits):
            new_str = ''
            for word in repeat_str.split():
                newWord = word
                if "#" in word:
                    newWord = "#" + str(times + 1) + word[1:]
                new_str += newWord + ' '
            send_to_screen(new_str[:len(new_str) - 1])
            atk_handler(char_name, target_name, atk_dict)
    elif isinstance(target_name, int) and target_name != 4:
        for side in faction:
            if char_name in faction[side]:
                team = faction[side]
            else:
                not_team = faction[side]
        lis = ([char_name] if target_name == 1 else
                team if target_name == 2 else
                not_team if target_name == 3 else
                [])
        for char in lis:
            atk_handler(char_name, char,
                    character.format_string_in_dict(
                        deepcopy(atk_dict), char))
    else:
        atk_handler(char_name, target_name, atk_dict)

def atk_handler(char_name, target_name, atk_dict):
    '''
    handles every valid atk and sends it to the
    right function
    '''

    global wait_for_hit, wait_for_next_turn
    if (everyone[target_name].check_if_dead() and
            "wait_for_next_turn" not in atk_dict):
        send_to_screen(char_name + "'s attack failed.")
        return 0
    elif char_name in target_lose_turn:
        send_to_screen(target_lose_turn.pop(char_name))
        return 0
    elif not checkAcc(char_name, target_name, atk_dict):
        send_to_screen(char_name + " missed!")
    else:
        if target_name in wait_for_hit:
            target_atk = wait_for_hit.pop(target_name)
            wait_dict = target_atk.pop("wait_for_hit")
            recieve_dmg = wait_dict["recieve_dmg"]
            counter_atk = wait_dict.get("counter_atk", False)
            if recieve_dmg:
                mod_atk(char_name, target_name, atk_dict)
            else:
                recieve_str = wait_dict["recieve_str"]
                send_to_screen(recieve_str)
            if counter_atk:
                target_atk["atk_str"] = wait_dict[
                        "counter_atk_str"]
                target_atk["target"] = char_name
                attack(target_name, target_atk)
        elif target_name in wait_for_next_turn:
            recieve_dmg = wait_for_next_turn[target_name][
                    "wait_for_next_turn"]["recieve_dmg"]
            if recieve_dmg:
                mod_atk(char_name, target_name, atk_dict)
            else:
                send_to_screen(char_name + " missed!")
        else:
            mod_atk(char_name, target_name, atk_dict)

def checkAcc(char_name, target_name, atk_dict):
    '''
    checks if the atk missed or not
    '''

    global everyone
    character = everyone[char_name]
    target = everyone[target_name]
    base_acc = atk_dict.get("base_acc", 0)
    char_acc = character.stats["acc"]
    target_eva = target.stats["eva"]
    acc = (base_acc/100.0) * (char_acc/target_eva)
    #make sure target is not on same team
    team = (faction["allies"] if char_name in faction[
        "allies"] else faction["enemies"])
    same_team = True if target_name in team else False
    r = random()
    if not r < acc and not same_team:
        return False
    return True

def mod_atk(char_name, target_name, atk_dict):
    '''
    handles dmg and stat modifications

    dmg can be seen as a stat modification to hp
    '''
    global everyone, target_lose_turn
    target = everyone[target_name]
    mod_dict = atk_dict.get("mod", {})
    lose = atk_dict.get("target_lose_turn", False)
    if lose:
        target_lose_turn[target_name] = lose
    if mod_dict:
        mod_string = atk_dict.get("mod_str")
    else:
        mod_string = ''
    dmg = calc_dmg(char_name, target_name, atk_dict)
    if dmg:
        mod_dict["hp"] = dmg
        send_to_screen("%s took %d damage!" %(target_name, -dmg))
    absorb_dict = atk_dict.get("absorb", False)
    if absorb_dict:
        absorb(char_name, dmg, absorb_dict)
    target.stat_modifier(mod_dict)
    if mod_string:
        send_to_screen(mod_string)
    bury_if_dead(target_name)

def calc_dmg(char_name, target_name, atk_dict):
    '''
    calculates dmg based on target defense
    character strength base attack power
    of attack and character luck
    '''

    global everyone
    character = everyone[char_name]
    target = everyone[target_name]
    mag_atk = atk_dict.get("mp_used", 0)
    atk = character.stats["ma" if mag_atk else "str"]
    defe = target.stats["md" if mag_atk else "def"]
    lck = character.check_if_lucky()
    #defending character is given advantage
    atk_def_ratio = ((atk * 1.0) / (defe * 2.0)) * lck
    base_atk = (atk_dict.get("base_atk", 0) / 100.0) * atk
    if not base_atk:
        return 0
    if lck == 2:
        send_to_screen('That\'s gonna leave a mark!')
    return int(round(-1 * (atk_def_ratio + base_atk)
        * atk_def_ratio))

def absorb(char_name, dmg, absorb_dict):
    '''
    calculates how much of the dmg is absorbed
    and sends it to the character
    '''

    global everyone
    character = everyone[char_name]
    stat = absorb_dict["stat_benefit"]
    factor = absorb_dict["factor"]
    mod = int(round((factor / 100.0) * -dmg))
    character.stat_modifier({stat: mod})
    send_to_screen("%s gained %d %s!" %(char_name, mod, stat))

#def status_effect():
#    pass

def bury_if_dead(char_name):
    '''
    removes character from game once the character
    has been declared dead
    '''

    global everyone, faction
    character = everyone[char_name]
    if character.check_if_dead():
        send_to_screen("%s died." %(char_name))
        for side in faction:
            if char_name in faction[side]:
                faction[side].remove(char_name)
                break

#check for end status
def check_if_end(player):
    '''
    checks if the battle is finished

    it does not however check who won
    '''
    enemies = faction["enemies"]
    if everyone[player].check_if_dead() or not enemies:
        return True
    return False

def test():
    '''
    This is to debug the battle features

    currently only supports spectating a battle
    between AI's
    '''

    #You can pass the build argument as a bunch of kwargs
    MasaYume = player.Player(name = "MasaYume",
            equipment = {
                "head": "cap",
                "body": "rusty chainmail",
                "right_hand": "gauntlet",
                "left_hand": "dagger",
                "legs": "leather greaves"
                },
            skills = ["speed punch", "zen punch", "backstab"]
            )
    #Or you can pass it as a dictionary just don't forget the **
    #in front of the dict
    Brandon = anpc.ANPC(**{"name": "Brandon",
        "equipment": {
            "head": "cap",
            "body": "rusty chainmail",
            #this is two-handed so both_hands are used
            #but you can litterally put anything for
            #two-handed weapons as long as it is different
            #from the other body parts
            "both_hands": "rifle",
            "legs": "leather greaves"
            },
        "skills": ["smokescreen", "trip", "focus shot"]
        })
    typical_warrior = anpc.ANPC(**{"name": "Kid Authur",
        "equipment": {
            "head": "cap",
            "body": "rusty chainmail",
            "right_hand": "sword",
            "left_hand": "wooden shield",
            "legs": "leather greaves"
            },
        "skills": ["warcry", "counter strike", "shield bash"]
        })
    typical_archer = anpc.ANPC(**{"name": "elf",
        "equipment": {
            "head": "cap",
            "body": "rusty chainmail",
            #I did say anything, right?
            "anything": "bow",
            "legs": "leather greaves"
            },
        "skills": ["smokescreen", "arrow barrage", "spreadshot"]
        })
    demon = anpc.ANPC(name = "demon")
    dragon = anpc.ANPC(name = "dragon")
    basilisk = anpc.ANPC(name = "basilisk")
    #basilisk vs dragon ;)
    return battle(MasaYume, [], [demon])

if __name__ == "__main__":
    auto_test = 0
    if auto_test:
        quiet = True
        wins = 0
        for x in range(auto_test):
            wins += test()
        #This number is usefull for balancing weapons and skills
        print wins
    else:
        test()
