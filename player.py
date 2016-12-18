#!/usr/bin/python2
#
#~~Player Functions~~

from superRandom import super_randint, super_choice
import main
from character import Character
from items import Item, items
from copy import deepcopy
import skills

class Player(Character):
    '''
    This class is specifically for the player and thus contain
    methods that will be used specifically for the player
    '''

    def __eq__(self, other):
        """
        Used to check if two player objects are equal
        using a couple important attributes

        :other: The other player
        :return: boolean value, true for equal, false for not

        """
        return (
            self.name == other.name and
            self.equipment == other.equipment and
            self.skills == other.skills and
            self.skill_bag == other.skill_bag and
            self.inventory == other.inventory and
            self.stats == other.stats
                )

    def build(self, build):
        super(Player, self).build(build)
        for key in ("steps", "run_away", "dragon_attack",
                "basilisk_attack"):
            self.stats[key] = build.get(key, 0)

    def update(self, load_player):
        self.name = load_player.name
        self.equipment = load_player.equipment
        self.skills = load_player.skills
        self.skill_bag = load_player.skill_bag
        self.inventory = load_player.inventory
        self.stats = load_player.stats

    def HUD(self):
        '''
        Heads Up Display designed to keep important
        information at the top of the screen
        '''

        translate = main.player_friendly_stats
        choices = ["hp", "sp", "mp", "lvl", "gold"]
        options = []
        for stat in choices:
            stat_val = self.stats[stat]
            try:
                stat_max = self.stats["max_" + stat]
                options.append("%d/%d" %(stat_val, stat_max))
            except KeyError:
                options.append("%d" % stat_val)
        print main.create_menu(
                prompt = self.name,
                choices = [translate[stat] for stat in choices],
                options = options
                )

    def validate_input(self, prompt = (), choices = (), menu_choices = (),
            options = (), invalid_prompt = "Invalid choice.", show_HUD = False,
            enter_option = True, make_menu = True, combine = '',
            YN_menu = False):
        '''
        displays menu and validates input

        prompt is what is repeated every loop
        choices is a tuple of choices for user
        menu_choices represents the choices tuple to be passed to the create_menu function
        options is used to create menu
        invalid_prompt is what will be said when input is invalid
        show_HUD is for when you want the HUD to appear too
        enter_option is for if you want an empty choice appended
        make_menu is to automatically create menu with input validation
        combine is for any info board that needs to go with the menu
        YN_menu is for making yes or no menues
        '''

        if YN_menu:
            choices = ('y','n')
            prompt = main.create_menu(
                    prompt = prompt,
                    choices = choices,
                    options = ('yes','no'),
                    enter_option = enter_option
                    )
            invalid_prompt = "Type either 'y' or 'n'."
        elif make_menu:
            if not menu_choices:
                menu_choices = choices
            prompt = main.create_menu(
                    prompt = prompt,
                    choices = menu_choices,
                    options = options,
                    enter_option = enter_option
                    )
        if combine:
            prompt = main.combine(combine, prompt)
        if enter_option:
            choices = list(choices)
            choices.append('')
        while 1:
            main.clearscreen(self if show_HUD else None)
            answer = raw_input(prompt).lower()
            if answer not in choices:
                print invalid_prompt
                main.confirm()
            else:
                return answer

    def validate_exp(self):
        '''
        checks to see if player should lvl up
        or not and then increases lvl if they should
        '''

        #continue lvling up until the below is false
        while self.stats["exp"] >= self.stats["exp_needed"]:
            main.clearscreen()
            before_stats = deepcopy(self.stats)
            self.lvl_up()
            after_stats = deepcopy(self.stats)
            body = ''
            #dictionaries dont save key order so I have to order them
            for stat in ("hp","sp","mp","def","str","md",
                    "ma","spe","lck"):
                if ("max_" + stat) in self.stats:
                    b_stat = before_stats["max_" + stat]
                else:
                    b_stat = before_stats[stat]
                a_stat = after_stats[stat]
                stat = main.player_friendly_stats[stat].capitalize()
                if b_stat != a_stat:
                    body += ("%s: %d --> %d\n"%(stat, b_stat, a_stat))
            body = body[:len(body) - 1] #remove last \n
            print main.create_info_board(
                    heading = ("You Leveled Up To Level %d!!!"
                        % self.stats['lvl']),
                    body = body
                    )
            main.confirm()

    def battle_prompt(self, allies = (), enemies = ()):
        '''
        Prompts for choice during battle whether it be a skill
        or an item
        '''

        while 1:
            action = self.validate_input(
                    prompt = "What do you want to do?",
                    choices = ("a", "s", "i", "r"),
                    options = ("attack", "skills", "inventory", "run"),
                    show_HUD = True,
                    enter_option = False
                    )
            if action == 'a':
                return self.target_prompt(self.reg_atk,
                        '', allies, enemies)
            elif action != 'r':
                if 's' in action:
                    attribute = ("equipped skills battle", skills.Skill)
                else:
                    attribute = ("inventory battle", Item)
                while 1:
                    sub_menu, options = self.list_attribute(attribute[0],
                            return_options = True)
                    attack = self.validate_input(
                            prompt = sub_menu,
                            choices = [str(x+1) for x in
                                range(len(options))],
                            make_menu = False
                            )
                    if attack:
                        constructor = attribute[1]
                        attack = constructor(options[int(attack) - 1])
                        answer = self.validate_input(
                                prompt = "Do you want to use this?",
                                combine = attack.describe_self(
                                    self.inventory.get(attack.name, 0)),
                                YN_menu = True
                                )
                        if answer == 'y':
                            if action == 'i':
                                self.edit_inv(attack.name, 1, True)
                                item_dict = attack.effect
                                if not item_dict.get('target', 0):
                                    return self.target_prompt(
                                            item_dict,
                                            attack.name, allies, enemies)
                                else:
                                    return item_dict
                            elif action == 's':
                                skill_dict = attack.effect
                                if self.SPMP_handle(skill_dict):
                                    return self.target_prompt(skill_dict,
                                            attack.name, allies, enemies)
                                else:
                                    print ("\nYou don't have enough "
                                            "sp or mp to do that")
                                    main.confirm()
                    else:
                        break
            else:
                return "run"

    def target_prompt(self, atk, atk_name, allies, enemies):
        '''
        prompts for target choice
        '''

        if (len(allies) == 1) and (len(enemies) == 1):
            return self.format_atk(deepcopy(atk), enemies[0])
        info_A = ''
        if len(allies) - 1:
            info_A = main.create_info_board(
                    heading = "Allies",
                    body = '\n'.join(allies)
                    )
        info_E = main.create_info_board(
                heading = "Enemies",
                body = '\n'.join(enemies)
                )
        target = self.validate_input(
                prompt = "who is your target?",
                choices = (enemies + 
                    (allies if (len(allies) - 1) else [])),
                show_HUD = True,
                make_menu = True,
                combine = (main.combine(info_A, info_E)
                    if info_A else info_E)
                )
        if target:
            return self.format_atk(deepcopy(atk), target, atk_name)
        else:
            return self.battle_prompt(allies, enemies)

    def list_attribute(self, attribute, part = "", prompt = "", return_options = False):
        '''
        lists a certain listable attribute like inventory
        or equipment

        The part kwarg is for the name of the equipment part
        like right hand, head, etc
        '''

        main.clearscreen()
        if "sk" in attribute:
            skill_list = []
            if "equi" in attribute:
                if "attle" in attribute:
                    skill_list = filter( lambda x: x, self.skills )
                else:
                    skill_list = [skill if skill else "Empty skill slot"
                            for skill in self.skills]
                menu = main.create_menu(
                        prompt = ("Equipped Skills" if not prompt
                            else ("Equipped Skills", prompt)),
                        choices = [str(x+1) for x in range(len(skill_list))],
                        options = skill_list,
                        enter_option = True
                        )
            else:
                skill_list += self.skill_bag
                menu = main.create_menu(
                        prompt = ("Unequipped Skills" if not prompt
                            else ("Unequipped Skills", prompt)),
                        choices = [str(x+1) for x in range(len(skill_list))],
                        options = skill_list,
                        enter_option = True
                        )
            string = menu
            if return_options:
                string = [string, skill_list]
        elif "equi" in attribute:
            if "un" in attribute:
                from equipment import Equipment
                title = part.replace('_', ' ')
                inv_equip = []
                for item in self.inventory:
                    try:
                        item = Equipment(item)
                        if item.type == part or (
                                (item.equip_type == "weapons")
                                and ("hand" in part)):
                            inv_equip.append(item.name)
                    except KeyError:
                        continue
                string = main.create_menu(
                        prompt = (title if not prompt else
                            (title, prompt)),
                        choices = [str(x+1) for x in
                            range(len(inv_equip))],
                        options = inv_equip,
                        enter_option = True
                        )
                return (string, inv_equip)
            else:
                choices = []
                options = []
                for part, equipment in self.equipment.items():
                    part = part.replace("_", " ")
                    choices.append(part)
                    options.append(equipment.name if equipment
                            else "None")
                string = main.create_menu(
                        prompt = ("Equipment" if not prompt else
                            ("Equipment", prompt)),
                        choices = choices,
                        options = options,
                        enter_option = True
                        )
                return (string, choices + options)
        elif "inv" in attribute:
            options = []
            allow = []
            if "attle" in attribute:
                allow = ["battle", "anywhere"]
            for item in self.inventory.keys():
                try:
                    if allow and (Item(item).type in allow):
                        options.append(item)
                except KeyError:
                    continue
            string = main.create_menu(
                    prompt = ("Inventory" if not prompt
                        else ("Inventory", prompt)),
                    choices = [str(x+1) for x in 
                        range(len(options))],
                    options = options,
                    enter_option = True
                    )
            if return_options:
                string = [string, options]
        elif "sta" in attribute:
            choices = []
            options = []
            #dictionaries dont save key order so I have to order them
            for stat in ("hp","sp","mp","def","str","md",
                    "ma","spe","lck","acc","eva","lvl",
                    "exp","gold"):
                value = self.stats[stat]
                if stat in main.player_friendly_stats:
                    choices.append(main.player_friendly_stats[
                        stat])
                    options.append(str(value))
            string = main.create_menu(
                    prompt = "Stats",
                    choices = choices,
                    options = options
                    )
        return string

    def view_inv(self):
        '''
        Shows player inventory and allows for in depth
        information and out of battle use of items
        '''

        while 1:
            menu = self.list_attribute("inventory",
                    prompt = ("What do you want to check out?"
                        if self.inventory else "")
                    )
            answer = self.validate_input(
                    prompt = menu,
                    choices = [str(x+1) for x in
                        range(len(self.inventory))],
                    make_menu = False,
                    show_HUD = True
                    )
            if answer:
                item = self.inventory.keys()[int(answer)-1]
            else:
                break
            main.clearscreen(self)
            try:
                from items import Item
                item = Item(item)
            except KeyError:
                from equipment import Equipment
                item = Equipment(item)
            quantity = self.inventory[item.name]
            info_board = item.describe_self(quantity)
            if isinstance(item, Item):
                if "any" in item.type:
                    answer = self.validate_input(
                            prompt = "Would you like to use this item?",
                            combine = info_board,
                            YN_menu = True,
                            show_HUD = True
                            )
                    if answer == "y":
                        self.use_item(item.name)
                else:
                    print info_board
                    main.confirm()
            elif isinstance(item, Equipment):
                self.equip_unequipped_equipment(item, quantity = quantity)

    def equip_unequipped_equipment(self, equip, part = "", quick = False,
            quantity = 0):
        '''
        allows the player to equip unequipped equippment
        '''
        #obtain equip
        from equipment import Equipment
        if not isinstance(equip, Equipment) :
            equip = Equipment(equip)

        #equip details and option to equip
        answer = self.validate_input(
                prompt = "Do you want to equip this?",
                combine = equip.describe_self(quantity),
                YN_menu = True
                )
        if answer == 'y':
            #choose where if weapon
            if (not part) and (equip.equip_type == "weapons" and
                    equip.hands_needed != 2):
                #show currently equipped items in right and left hand
                #allow player to choose which hand
                hands = ["right_hand", "left_hand"]
                options = [h.replace("_", " ") for h in hands]
                equip_name_list = [self.equipment[h].name for h in hands]
                answer = self.validate_input(
                        prompt = "Which hand?",
                        options = options,
                        menu_choices = equip_name_list,
                        choices = options + equip_name_list
                        )
                #get hand name if equip name is chosen
                if answer and answer not in options:
                    part = hands[equip_name_list.index(answer)]
                elif answer:
                    part = answer.replace(" ", "_")
                else:
                    return #go back
            elif (not part):
                if equip.equip_type == "weapons" and equip.hands_needed == 2:
                    part = ["right_hand", "left_hand"]
                else:
                    part = equip.type
            if not isinstance(part, list):
                parts = [part]
            else:
                parts = part
                part = parts[0]

            #if spot filled show current equip
            if not quick and self.equipment[part]:
                #ask to replace
                combine_prompt = main.combine(*[self.equipment[part].describe_self()
                    for part in parts])
                grammar_fix = " this?" if len(parts) == 1 else " these?"
                answer = self.validate_input(
                        prompt = "Do you want to replace" + grammar_fix,
                        combine = combine_prompt,
                        YN_menu = True
                        )
                if answer != "y":
                    return #go back

            #equip
            if (equip.equip_type == "armour" or
                (equip.equip_type == "weapons" and
                    self.validate_weapon(equip.type, part))):
                self.equip(equip, part)
                print "\n%s was equipped." %(equip.name)
                main.confirm()
            return 'y'

    def view_equip(self):
        '''
        Shows currently equipped items and allows for equipping
        of equipment in inventory
        '''
        while 1:
            menu, choices = self.list_attribute(
                    "equipment",
                    prompt = "What do you want to check out?"
                    )
            equip_name = self.validate_input(
                    prompt = menu,
                    choices = choices,
                    make_menu = False,
                )
            if equip_name:
                while 1:
                    for part, equip in self.equipment.items():
                         if ((equip and equip.name == equip_name) or
                                 (part.replace('_',' ') == equip_name)):
                            break
                    else:
                        equip = None
                    dequip_ability = (equip and equip.name != "bare")

                    title = "%s--%s" %(part.replace('_',' '),
                        equip.name.capitalize() if equip else "None")
                    question = "Would you like to equip something here"
                    question += ("? " if not dequip_ability
                            else " or dequip this item? ")

                    if dequip_ability:
                        choices = ("e",'d')
                        options = ('equip','dequip')
                    else:
                        choices = ('y','n')
                        options = ('yes', 'no')
                    if not equip:
                        equip_info = ''
                    else:
                        equip_info = equip.describe_self()
                    answer = self.validate_input(
                            prompt = (title, question),
                            choices = choices,
                            options = options,
                            make_menu = True,
                            combine = equip_info
                            )
                    if not answer or answer == 'n':
                        break
                    elif answer == 'y':
                        answer = 'e'
                    if answer == 'e':
                        while 1:
                            prompt = "What do you want to check out?"
                            menu, equip_list = self.list_attribute(
                                    "unequipped equipment",
                                    part, prompt)
                            unequip_name = self.validate_input(
                                    prompt = menu,
                                    choices = [str(x+1) for x in
                                        range(len(equip_list))],
                                    make_menu = False
                                    )
                            if not unequip_name:
                                break
                            else:
                                answer = self.equip_unequipped_equipment(
                                        equip_list[int(unequip_name)-1],part,True)
                                if answer == 'y':
                                    break
                        if answer == 'y': #break again after equip
                            break
                    elif answer == 'd' and (equip.equip_type == "armour" or
                            (equip.equip_type == "weapons" and
                                self.validate_weapon("fist", part))):
                        self.equip(equip, part, True)
                        print "\n%s was dequipped." %(equip.name)
                        main.confirm()
                        break
            else:
                break

    def validate_skills(self, weapon_type = None, autoremove = False,
            skill_type = ""):
        '''
        checks if currently equipped skills match types
        with currently equipped weapons or specific weapon
        type, and depending on flag removes skills from
        skill list

        can also validate specific skills
        '''

        if not weapon_type:
            weapon_type = []
            for side in ("left", "right"):
                equip = self.equipment[side + "_hand"]
                if equip:
                    weapon_type.append(equip.type)
        weapon_type.append("all")
        if skill_type:
            if skill_type in weapon_type:
                return True
            else:
                return False
        remove_skills = []
        for skill_name in self.skills:
            if skill_name and (skills.Skill(skill_name)).type not in weapon_type:
                remove_skills.append(skill_name)
        if not autoremove:
            return remove_skills
        else:
            if remove_skills:
                for skill_name in remove_skills:
                    self.equip_skill(skill_name, True)
                return True
            return False

    def validate_weapon(self, weapon_type, hand = "right_hand",
            two_hands = False):
        '''
        warns player of the removal of skills because of
        weapons about to be equipped
        '''

        #3 possibilities
        #1 handed weapon replace 2 handed weapon
        #1 handed weapon replaces 1 handed weapon
        #2 handed weapon replaces 1 handed weapon

        if not two_hands:
            if self.equipment["right_hand"].hands_needed == 2:
                remove_skills = self.validate_skills([weapon_type, "fist"])
            else:
                hands = ("right_hand", "left_hand")
                other_hand = hands[abs(hands.index(hand) - 1)]
                remove_skills = self.validate_skills([weapon_type,
                    self.equipment[other_hand].type])
        else:
            remove_skills = self.validate_skills([weapon_type])
        if remove_skills:
            #warn player
            info = main.create_info_board(
                    heading = ("If you do this, the following skills "
                        "will be removed"),
                    body = "\n".join(remove_skills)
                    )
            answer = self.validate_input(
                    prompt = "Are you sure you want to do this?",
                    combine = info,
                    YN_menu = True
                    )
            if "y" in answer:
                for skill_name in remove_skills:
                    self.equip_skill(skill_name, True)
                return True
            else:
                return False
        else:
            return True #True means it is ok to equip

    def choose_skill(self, equipped = True, prompt = ''):
        '''
        displays unequipped skills or equipped skills
        and outputs user choice
        '''

        if equipped:
            menu = self.list_attribute("equipped skills",prompt)
            choice = self.validate_input(
                    prompt = menu,
                    choices = [str(x+1) for x in range(5)],
                    make_menu = False,
                    )
        else:
            menu = self.list_attribute("skills",prompt)
            choice = self.validate_input(
                prompt = menu,
                choices = [str(x+1) for x in
                    range(len(self.skill_bag))],
                make_menu = False,
                )
        return choice

    def equip_unequipped_skill(self, prompt = '', replace = None):
        '''
        allows the player to choose a unequipped skill,
        see info on skill and equip the skill
        '''

        #choose skill from skill_bag
        choice = self.choose_skill(
                equipped = False,
                prompt = prompt)
        if not choice:
            return 0 #go back
        else:
            skill_name = self.skill_bag[int(choice) - 1]
        skill = skills.Skill(skill_name)

        #display unequipped skill info
        if not self.validate_skills(skill_type = skill.type):
            main.clearscreen()
            skill_info = skill.describe_self(
                    other = "\nYou cannot equip this "
                    "TYPE of skill.")
            print skill_info
            main.confirm()
        else:
            skill_info = skill.describe_self()
            answer = self.validate_input(
                    prompt = "Would you like to equip this skill?",
                    YN_menu = True,
                    combine = skill_info
                    )

            #equip unequipped skill
            if answer == "y":
                if replace:
                    self.equip_skill(replace.name, True)
                    self.equip_skill(skill.name)
                    print ("%s was dequipped and %s was equipped."
                            %(replace.name.capitalize(),
                            skill.name.capitalize()))
                    return 'y'
                elif self.equip_skill(skill.name):
                    print "%s was equipped." % skill.name.capitalize()
                    main.confirm()
                    return 'y'
                else:
                    return skill #warning
        return 1 #next iteration

    def view_skills(self):
        '''
        Displays skills and allows for in depth info on each
        skill and the equipping and dequipping of skills
        '''

        global skills
        while 1:
            section = self.validate_input(
                    prompt = ("Skills", "What do you want to see?"),
                    choices = ("u", "e"),
                    options = ("Unequipped Skills", "Equipped Skills"),
                    invalid_prompt = ("Please type 'u' for"
                        " unequipped or 'e' for equipped."),
                    )
            if not section:
                return
            gen_prompt = "What do you want to check out?"
            while 1:
                if section == "u":
                    action = self.equip_unequipped_skill(
                            prompt = (gen_prompt if
                                self.skill_bag else ''))
                    if not action:
                        break
                    elif action == 1 or action == 'y':
                        continue
                    else:
                        skill = action
                        while 1:
                            warning = main.create_info_board(
                                    heading = "Warning",
                                    body = ("5 skills is the max amount "
                                        "of skills\nyou can have equipped. "
                                        "To equip another skill,\nyou must "
                                        "dequip an equipped skill."
                                        )
                                    )
                            sub_menu = self.list_attribute(
                                    "equipped skills",
                                    prompt = gen_prompt.replace("check out",
                                        "replace")
                                    )
                            sub_choice = self.validate_input(
                                prompt = main.combine(warning, sub_menu),
                                choices = [str(x+1) for x in range(5)],
                                make_menu = False
                                )
                            if not sub_choice:
                                break
                            else:
                                skill_name = self.skills[int(sub_choice) - 1]
                            re_skill = skills.Skill(skill_name)
                            re_skill_info = re_skill.describe_self()
                            answer = self.validate_input(
                                    prompt = ("Would you like to "
                                        "replace this skill?"),
                                    YN_menu = True,
                                    combine = re_skill_info
                                    )
                            if answer == 'y':
                                self.equip_skill(re_skill.name, True)
                                self.equip_skill(skill.name)
                                print ("\n%s was dequiped and %s was equipped."
                                        %(re_skill.name.capitalize(),
                                            skill.name.capitalize()))
                                main.confirm()
                                break
                else:
                    #choose from equipped skills
                    choice = self.choose_skill(
                            prompt = (gen_prompt if self.skills else ""))
                    if not choice:
                        break
                    try:
                        skill_name = self.skills[int(choice) - 1]
                        skill = skills.Skill(skill_name)
                    except KeyError:
                        skill_name = ""
                    if skill_name:
                        while 1:
                            #choose between replace skill or dequip
                            skill_info = skill.describe_self()
                            choice = self.validate_input(
                                    prompt = ("Would you like to equip "
                                        "something else here or dequip "
                                        "this skill?"),
                                    choices = ("e", "d"),
                                    options = ('equip','dequip'),
                                    make_menu = True,
                                    combine = skill_info
                                    )
                            if not choice:
                                break
                            elif choice == "e":
                                action = 1
                                while 1:
                                    action = self.equip_unequipped_skill(
                                            prompt = (gen_prompt if
                                                self.skill_bag else ""),
                                            replace = skill)
                                    if not action or action == 'y':
                                        break
                                if action == 'y':
                                    break
                            else:
                                self.equip_skill(skill_name, True)
                                print "\n%s was dequipped." %(
                                        skill_name.capitalize())
                                main.confirm()
                                break
                    else:
                        while 1:
                            answer = self.validate_input(
                                    prompt = ("This is an empty slot",
                                        "Do you want to equip something "
                                        "here?"),
                                    YN_menu = True
                                    )
                            if answer == 'y':
                                while 1:
                                    action = self.equip_unequipped_skill(
                                            prompt = (gen_prompt if
                                                self.skill_bag else ""))
                                    if not action or action == 'y':
                                        break
                            break

    def view_stats(self):
        '''
        Displays current stats
        '''

        print self.list_attribute("stats")
        main.confirm()

    def use_item(self, item):
        '''
        Use item and remove it from inventory
        '''

        Item(item).use(self)
        self.edit_inv(item, 1, True)
        main.confirm()

    def low_health(self):
        '''
        Warns user of low health
        '''

        health = self.stats["hp"]
        potions = self.inventory["potion"]
        info = main.create_info_board(
                heading = "DANGER!!!!",
                body = ("Your health is currently at %d,\n"
                "and you currently have %d potions in your\n"
                "inventory." % (health, potions))
                )
        answer = self.validate_input(
            prompt = "Would you like to use one?",
            YN_menu = True,
            combine = info,
            enter_option = False
            )
        if answer == 'y':
            self.use_item("potion")
        elif answer == 'n':
            print "\nOk tough guy."
            main.confirm()

    def gold_handle(self, cost):
        '''
        handles gold transactions
        '''

        if self.stats["gold"] < cost:
            return False
        self.stat_modifier({"gold": -cost})
        return True
