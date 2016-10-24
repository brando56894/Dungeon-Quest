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

    def validate_input(self, prompt = "", choices = (),
            invalid_prompt = "", show_HUD = False,
            enter_choice = False):
        '''
        Validates input by using a while loop and returns valid
        input

        prompt is what is repeated every loop
        choices is a tuple of choices for user
        invalid_prompt is what will be said when input is invalid
        show_HUD is for when you want the HUD to appear too
        enter_choice is for if you want an empty choice appended
        '''

        if enter_choice:
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


    def battle_prompt(self, allies = [], enemies = []):
        '''
        Prompts for choice during battle whether it be a skill
        or an item
        '''

        while 1:
            main.clearscreen(self)
            choices = ("a", "s", "i", "r")
            menu = main.create_menu(
                    prompt = "What do you want to do?",
                    choices = choices,
                    options = ("attack", "skills", "inventory", "run")
                    )
            action = self.validate_input(
                    prompt = menu,
                    choices = choices,
                    invalid_prompt = "Invalid choice."
                    )
            if action == 'a':
                return self.target_prompt(self.reg_atk,
                        '', allies, enemies)
            elif action != 'r':
                if 's' in action:
                    attribute = ("equipped skills", self.skills)
                else:
                    attribute = ("inventory", self.inventory)
                while 1:
                    sub_menu = self.list_attribute(attribute[0])
                    attack = self.validate_input(
                            prompt = sub_menu,
                            choices = [str(x+1) for x in
                                range(len(attribute[1]))],
                            invalid_prompt = "Invalid choice.",
                            enter_choice = True
                            )
                    if attack:
                        if action == 'i':
                            self.edit_inv(attack, 1, True)
                            item = Item(attack)
                            item_dict = item.effect
                            if not item_dict.get('target', 0):
                                return self.target_prompt(
                                        item.effect,
                                        attack, allies, enemies)
                            else:
                                return item_dict
                        elif action == 's':
                            skill_dict = skills.Skill(attack).effect
                            #what if target is you
                            if self.SPMP_handle(skill_dict):
                                return self.target_prompt(skill_dict,
                                        attack, allies, enemies)
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
        main.clearscreen(self)
        if len(allies) - 1:
            info_A = main.create_info_board(
                    heading = "Allies",
                    body = '\n'.join(allies)
                    )
        info_E = main.create_info_board(
                heading = "Enemies",
                body = '\n'.join(enemies)
                )
        menu = main.create_menu(
                prompt = "Who is your target?",
                enter_option = True
                )
        combination_display = main.combine(
                info_A, info_B, menu)
        target = self.validate_input(
                prompt = combination_display,
                choices = (enemies + 
                    (allies if (len(allies) - 1) else [])),
                invalid_prompt = "Invalid choice"
                )
        if target:
            return self.format_atk(deepcopy(atk), target, atk_name)
        else:
            return self.battle_prompt(allies, enemies)

    def list_attribute(self, attribute, part = "", prompt = ""):
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
                skill_list = [skill if skill else "Empty skill slot"
                        for skill in self.skills]
                menu = main.create_menu(
                        prompt = ("Equipped Skills" if not prompt
                            else ("Equipped Skills", prompt)),
                        choices = [str(x+1) for x in range(5)],
                        options = skill_list,
                        enter_option = True
                        )
            else:
                skill_list += self.skill_bag
                menu = main.create_menu(
                        prompt = ("Skills" if not prompt
                            else ("Skills", prompt)),
                        choices = [str(x+1) for x in range(len(skill_list))],
                        options = skill_list,
                        enter_option = True
                        )
            string = menu
        elif "equi" in attribute:
            if "inv" in attribute:
                from equipment import Equipment
                title = part.replace('_', ' ')
                inv_equip = []
                for item in self.inventory:
                    try:
                        Equipment(item)
                        inv_equip.append(item)
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
                        )
                return (string, choices + options)
        elif "inv" in attribute:
            options = []
            for item, quantity in self.inventory.items():
                options.append(item)
            string = main.create_menu(
                    prompt = ("Inventory" if not prompt
                        else ("Inventory", prompt)),
                    choices = [str(x+1) for x in 
                        range(len(self.inventory))],
                    options = options,
                    enter_option = True
                    )
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
                    options.append(value)
            string = main.create_menu(
                    prompt = "Stats",
                    choices = choices,
                    options = options,
                    )
        return string

    def view_inv(self):
        '''
        Shows player inventory and allows for in depth
        information and out of battle use of items
        '''

        while 1:
            prompt = self.list_attribute("inventory",
                    prompt = ("What do you want to check out?"
                        if self.inventory else "")
                    )
            answer = self.validate_input(
                    prompt = prompt,
                    choices = [str(x+1) for x in
                        range(len(self.inventory))],
                    invalid_prompt = "Invalid choice",
                    enter_choice = True,
                    )
            if answer:
                item = self.inventory.keys()[int(answer)-1]
            else:
                break
            main.clearscreen()
            try:
                from items import Item
                item = Item(item)
            except KeyError:
                from equipment import Equipment
                item = Equipment(item)
            info_board = item.describe_self(self.inventory[item.name])
            if isinstance(item, Item):
                display = "any" in item.type
                menu = main.create_menu(
                        prompt = ("Would you like to use this item?"
                            if display else ""),
                        choices = ('y', 'n') if display else (),
                        options = ('Yes', 'No') if display else (),
                        enter_option = True,
                        )
                prompt = main.combine(info_board, menu)
                if display:
                    answer = self.validate_input(
                            prompt = prompt,
                            choices = ('y','n',''),
                            invalid_prompt = ("Press type either"
                                " 'yes' or 'no'.")
                            )
                    if answer == "y":
                        self.use_item(item.name)
                else:
                    raw_input(prompt)
            else:
                print info_board
                main.confirm()

    def view_equip(self):
        '''
        Shows currently equipped items and allows for equipping
        of equipment in inventory
        '''

        while 1:
            info_board, choices = self.list_attribute("equipment")
            menu = main.create_menu(
                    prompt = "What do you want to check out?",
                    enter_option = True
                    )
            prompt = main.combine(info_board,menu)
            answer = self.validate_input(
                    prompt = prompt,
                    choices = choices,
                    invalid_prompt = "Invalid choice.",
                    enter_choice = True
                )
            if answer:
                part = ''
                while 1:
                    if not part:
                        for part, equip in self.equipment.items():
                            if equip and ((equip.name == answer) or
                                    (part.replace('_',' ') == answer)):
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
                    menu = main.create_menu(
                            prompt = (title, question),
                            choices = choices,
                            options = options,
                            enter_option = True
                            )
                    if dequip_ability:
                        equip_info = equip.describe_self()
                        prompt = main.combine(equip_info, menu)
                    else:
                        prompt = menu
                    answer = self.validate_input(
                            prompt = prompt,
                            choices = choices,
                            invalid_prompt = "Invalid choice.",
                            enter_choice = True
                            )
                    if not answer or answer == 'n':
                        break
                    elif answer == 'y':
                        answer = 'e'
                    if answer == 'e':
                        while 1:
                            prompt = "What do you want to check out?"
                            menu, equip_list = self.list_attribute(
                                    "part equipment in inventory",
                                    part, prompt)
                            answer = self.validate_input(
                                    prompt = menu,
                                    choices = [str(x+1) for x in
                                        range(len(equip_list))],
                                    invalid_prompt = "Invalid choice.",
                                    enter_choice = True
                                    )
                            if not answer:
                                break
                            else:
                                from equipment import Equipment
                                answer = equip_list[int(answer)-1]
                                equip = Equipment(answer)
                                equip_info = equip.describe_self()
                                menu = main.create_menu(
                                        prompt = "Do you want to equip this?",
                                        choices = ('y', 'n'),
                                        options = ('yes', 'no'),
                                        enter_option = True
                                        )
                                answer = self.validate_input(
                                        prompt = main.combine(equip_info, menu),
                                        choices = ('y','n'),
                                        invalid_prompt = "Invalid choice.",
                                        enter_choice = True
                                        )
                                if answer == 'y' and self.validate_equip(equip.type):
                                    self.equip(equip, part)
                                    print "\n%s was equipped." %(equip.name)
                                    main.confirm()
                                    break
                        if answer == 'y': #break again after equip
                            break
                    elif answer == 'd' and self.validate_equip("fist"):
                        self.equip(equip, part, True)
                        print "\n%s was dequipped." %(equip.name)
                        main.confirm()
                        break
            else:
                break

    def validate_skills(self, weapon_type = [], autoremove = False,
            skill_type = ""):
        '''
        checks if currently equipped skills match types
        with currently equipped weapons or specific weapon
        type, and depending on flag removes skills from
        skill list

        can also validate specific skills
        '''

        if not weapon_type:
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

    def validate_equip(self, weapon_type):
        '''
        warns player of the removal of skills because of
        weapons about to be equipped
        '''

        remove_skills = self.validate_skills([weapon_type])
        if remove_skills:
            #warn player
            info = main.create_info_board(
                    heading = ("If you do this, the following skills "
                        "will be removed"),
                    body = "\n".join(remove_skills)
                    )
            menu = main.create_menu(
                    prompt = "Are you sure you want to do this?",
                    choices = ('y','n'),
                    options = ('yes','no'),
                    enter_option = True
                    )
            answer = self.validate_input(
                    prompt = main.combine(info,menu),
                    choices = ("y", "n"),
                    invalid_prompt = "Please type either 'y' ot 'n'."
                    )
            if "y" in answer:
                for skill_name in remove_skills:
                    self.equip_skill(skill_name, True)
                return True
            else:
                return False
        else:
            return True #True means it is ok to equip

    def view_skills(self):
        '''
        Displays skills and allows for in depth info on each
        skill and the equipping and dequipping of skills
        '''

        global skills
        while 1:
            menu = main.create_menu(
                    prompt = ("Skills", "What do you want to see?"),
                    choices = ("U", "E"),
                    options = ("Unequipped", "Equipped"),
                    enter_option = True
                    )
            section = self.validate_input(
                    prompt = menu,
                    choices = ("u", "e"),
                    invalid_prompt = ("Please type 'u' for"
                        " unequipped or 'e' for equipped"),
                    enter_choice = True
                    )
            if not section:
                return

            gen_prompt = "What do you want to check out?"
            while 1:
                if section == "u":
                    menu = self.list_attribute("skills",
                            prompt = (gen_prompt if self.skill_bag else ""))
                    choice = self.validate_input(
                        prompt = menu,
                        choices = [str(x+1) for x in
                            range(len(self.skill_bag))],
                        invalid_prompt = "Invalid input.",
                        enter_choice = True
                        )
                    if not choice:
                        break
                    else:
                        skill_name = self.skill_bag[int(choice) - 1]

                    skill = skills.Skill(skill_name)
                    if not self.validate_skills(skill_type = skill.type):
                        main.clearscreen()
                        skill_info = skill.describe_self(
                                other = "You cannot equip this "
                                "TYPE of skill.")
                        main.confirm()
                        continue
                    else:
                        skill_info = skill.describe_self()
                        menu = main.create_menu(
                                prompt = "Would you like to equip this skill?",
                                choices = ('y','n'),
                                options = ('yes','no'),
                                enter_option = True
                                )
                        answer = self.validate_input(
                                prompt = main.combine(skill_info,menu),
                                choices = ("y", "n"),
                                invalid_prompt = "Please type 'y' or 'n'.",
                                enter_choice = True
                                )
                    if answer == "y":
                        if self.equip_skill(skill.name):
                            print "%s was equipped." % skill.name.capitalize()
                            main.confirm()
                            continue
                        else:
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
                                    prompt = main.combine(sub_menu, warning),
                                    choices = [str(x+1) for x in range(5)],
                                    invalid_prompt = "Invalid choice.",
                                    enter_choice = True
                                    )
                                if not sub_choice:
                                    break
                                else:
                                    skill_name = self.skills[int(sub_choice) - 1]
                                re_skill = skills.Skill(skill_name)
                                re_skill_info = re_skill.describe_self()
                                re_menu = main.create_menu(
                                        prompt = ("Would you like to "
                                            "replace this skill?"),
                                        choices = ('y','n'),
                                        options = ('yes','no'),
                                        enter_option = True
                                        )
                                answer = self.validate_input(
                                        prompt = main.combine(re_skill_info,
                                            re_menu),
                                        choices = ("y", "n"),
                                        invalid_prompt = "Please type 'y' or 'n'.",
                                        enter_choice = True
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
                    eq_list = self.list_attribute("equipped skills",
                            prompt = (gen_prompt if self.skills else ""))
                    choice = self.validate_input(
                            prompt = eq_list,
                            choices = [str(x+1) for x in range(5)],
                            invalid_prompt = "\nInvalid choice.",
                            enter_choice = True
                            )
                    if not choice:
                        break
                    try:
                        skill_name = self.skills[int(choice) - 1]
                        skill = skills.Skill(skill_name)
                    except KeyError:
                        skill_name = ""
                    if skill_name:
                        while 1:
                            skill_info = skill.describe_self()
                            question = main.create_menu(
                                    prompt = ("Would you like to equip "
                                        "something else here or dequip "
                                        "this skill?"),
                                    choices = ('e','d'),
                                    options = ('equip','dequip'),
                                    enter_option = True
                                    )
                            choice = self.validate_input(
                                    prompt = main.combine(
                                        skill_info, question),
                                    choices = ("e", "d"),
                                    invalid_prompt = "Invalid choice.",
                                    enter_choice = True
                                    )
                            if not choice:
                                break
                            elif choice == "e":
                                answer = ""
                                while 1:
                                    sub_menu = self.list_attribute(
                                            "skills",
                                            prompt = gen_prompt)
                                    sub_choice = self.validate_input(
                                            prompt = sub_menu,
                                            choices = [str(x+1) for x in
                                                range(len(self.skill_bag))],
                                            invalid_prompt = "\nInvalid choice.",
                                            enter_choice = True
                                            )
                                    if sub_choice:
                                        re_skill = skills.Skill(self.skill_bag[
                                            int(sub_choice) - 1])
                                        main.clearscreen()
                                        if not self.validate_skills(skill_type = re_skill.type):
                                            print re_skill.describe_self("You cannot "
                                                    "equip this TYPE of skill.")
                                            main.confirm()
                                        else:
                                            re_skill_info = re_skill.describe_self()
                                            YN_menu = main.create_menu(
                                                    prompt = ("Would you like "
                                                        "to equip this skill?"),
                                                    choices = ('y','n'),
                                                    options = ('yes','no'),
                                                    enter_option = True
                                                    )
                                            answer = self.validate_input(
                                                    prompt = main.combine(
                                                        re_skill_info,YN_menu),
                                                    choices = ("y", "n"),
                                                    invalid_prompt = ("Please type either"
                                                        " 'y' or 'n'."),
                                                    enter_choice = True
                                                    )
                                            if answer == 'y':
                                                self.equip_skill(skill.name, True)
                                                self.equip_skill(re_skill.name)
                                                print ("%s was dequipped and %s was equipped."
                                                        %(skill.name.capitalize(),
                                                        re_skill.name.capitalize()))
                                                main.confirm()
                                    if not sub_choice or answer == 'y':
                                        break
                                if answer == 'y':
                                    break
                            else:
                                self.equip_skill(skill_name, True)
                                print "\n%s was dequipped." %(
                                        skill_name.capitalize())
                                main.confirm()
                                break
                    else:
                        while 1:
                            menu = main.create_menu(
                                    prompt = ("This is an empty slot",
                                        "Do you want to equip something "
                                        "here?"),
                                    choices = ('y','n'),
                                    options = ('yes','no'),
                                    enter_option = True
                                    )
                            answer = self.validate_input(
                                    prompt = menu,
                                    choices = ('y','n'),
                                    invalid_prompt = "Please type either 'y' or 'n'.",
                                    enter_choice = True
                                    )
                            if answer == 'y':
                                while 1:
                                    sub_menu = self.list_attribute(
                                            "skills",
                                            prompt = gen_prompt)
                                    sub_choice = self.validate_input(
                                            prompt = sub_menu,
                                            choices = [str(x+1) for x in
                                                range(len(self.skill_bag))],
                                            invalid_prompt = "Invalid choice.",
                                            enter_choice = True
                                            )
                                    if sub_choice:
                                        skill = skills.Skill(
                                                self.skill_bag[int(sub_choice)-1])
                                        skill_info = skill.describe_self()
                                        YN_menu = main.create_menu(
                                                prompt = ("Would you like to "
                                                    "equip this skill?"),
                                                choices = ('y','n'),
                                                options = ('yes','no'),
                                                enter_option = True
                                                )
                                        answer = self.validate_input(
                                                prompt = main.combine(
                                                    skill_info, YN_menu),
                                                choices = ("y", "n"),
                                                invalid_prompt = ("Please type either"
                                                    " 'y' or 'n'."),
                                                enter_choice = True
                                                )
                                        if answer == 'y':
                                            self.equip_skill(skill.name)
                                            print "%s was equipped" % skill.name
                                            main.confirm()
                                    if not sub_choice or answer == 'y':
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
        if health <= 60 and potions > 0:
            info = main.create_info_board(
                    heading = "*****DANGER*****",
                    body = ("Your health is currently at %d, "
                    "and you currently have %d potions in your "
                    "inventory." % (health, potions))
                    )
            menu = main.create_menu(
                prompt = "Would you like to use one?",
                choices = ('y', 'n'),
                options = ('yes','no')
                )
            answer = self.validate_input(
                prompt = main.combine(info,menu),
                choices = ('y','n'),
                invalid_prompt = ("That was a 'yes' or 'no'"
                    "question."),
                enter_choice = True
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
