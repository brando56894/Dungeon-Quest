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
            invalid_prompt = "", show_HUD = False):
        '''
        Validates input by using a while loop and returns valid
        input

        prompt is what is repeated every loop
        choices is a tuple of choices for user
        invalid_prompt is what will be said when input is invalid
        '''

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

        #TODO:Standardize input validation when you fix menu
        while 1:
            main.clearscreen(self)
            string = "What do you want to do?\n-------------------\n"
            for option in ("attack", "skills", "inventory", "run"):
                string += option[:1].upper() + ')' + option[1:] + '\n'
            print string + '\n'
            action = raw_input("Choice: ").lower()
            if 'a' in action:
                return self.target_prompt(self.reg_atk,
                        '', allies, enemies)
            elif 's' in action or 'i' in action:
                if 's' in action:
                    attribute = ("equipped skills", self.skills)
                else:
                    attribute = ("inventory", self.inventory)
                while 1:
                    print ("%s\nPress Enter To Go Back\n" %(
                        self.list_attribute(attribute[0])[0]))
                    attack = raw_input("Choice: ").lower()
                    if attack in attribute[1]:
                        if 'i' in action:
                            self.edit_inv(attack, 1, True)
                            item = Item(attack)
                            item_dict = item.effect
                            if not item_dict.get('target', 0):
                                return self.target_prompt(
                                        item.effect,
                                        attack, allies, enemies)
                            else:
                                return itemDict
                        elif 's' in action:
                            skill_dict = skills.Skill(attack).effect
                            if self.SPMP_handle(skill_dict):
                                return self.target_prompt(skill_dict,
                                        attack, allies, enemies)
                        else:
                            print ("\nYou don't have enough "
                                    "sp or mp to do that")
                            main.confirm()
                    elif not attack:
                        return self.battle_prompt(allies, enemies)
                    else:
                        print "\nInvalid choice"
                        main.confirm()
            elif 'r' in action:
                return "run"
            else:
                print "\nInvalid choice."
                main.confirm()

    def target_prompt(self, atk, atk_name, allies, enemies):
        '''
        prompts for target choice
        '''

        #TODO:Standardize input validation when you fix menu
        while 1:
            if (len(allies) == 1) and (len(enemies) == 1):
                return self.format_atk(deepcopy(atk), enemies[0])
            main.clearscreen(self)
            display = ""
            if len(allies) - 1:
                display += ("Allies\n------------\n%s\n\n" %(
                        '\n'.join(allies)))
            display += ("Enemies\n------------\n%s\n\n" %(
                '\n'.join(enemies)))
            display += "Press Enter To Go Back\n"
            target = raw_input("%s\nWho is your target? " % display).lower()
            for char in allies + enemies:
                if target == char.lower():
                    return self.format_atk(deepcopy(atk), char, atk_name)
            if not target:
                return self.battle_prompt(allies, enemies)
            else:
                print "\nInvalid choice"
                main.confirm()

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
            string = (menu, skill_list)
        elif "equi" in attribute:
            if "inv" in attribute:
                from equipment import Equipment
                string = ("%s\n---------------\n" %(
                    part.replace('_', ' ').capitalize()))
                inv_equip = []
                for item in self.inventory:
                    try:
                        Equipment(item)
                        inv_equip.append(item)
                    except KeyError:
                        continue
                if inv_equip:
                    string += "%s\n" %('\n'.join(inv_equip))
                else:
                    string += "Y u no hav nuthing!!!\n"
                return (string, inv_equip)
            else:
                choices = []
                options = []
                for part, equipment in self.equipment.items():
                    part = part.replace("_", " ").capitalize()
                    choices.append(part)
                    options.append(equipment.name if equipment
                                else "None")
                string = main.create_menu(
                        prompt = "Equipment",
                        choices = choices,
                        options = options,
                        )
        elif "inv" in attribute:
            string = "Inventory\n----------------\n"
            if not self.inventory:
                string += "Y u no hav nuthing!!!\n"
            for item, quantity in self.inventory.items():
                string += "%s: %d\n" %(item, quantity)
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
                        stat].capitalize())
                    options.append(value)
            string = main.create_menu(
                    prompt = "Stats",
                    choices = choices,
                    options = options,
                    )
        return string

    def view_inv(self, item = None):
        '''
        Shows player inventory and allows for in depth
        information and out of battle use of items
        '''

        print "%s\nPress Enter To Go Back\n" %(
                self.list_attribute("inventory"))
        if not item:
            answer = raw_input("\nWhat do you want to check out? "
                    if self.inventory else "").lower()
            if answer in self.inventory:
                item = answer
            elif answer:
                print "\nInvalid choice"
                main.confirm()
                self.view_inv()
                return
            else:
                return
        main.clearscreen()
        try:
            from items import Item
            item = Item(item)
        except KeyError:
            from equipment import Equipment
            item = Equipment(item)
        print ("%sQuantity: %d\n\nPress Enter "
                "To Go Back"
                %(item.describe_self(),
                    self.inventory[item.name]))
        if isinstance(item, Item):
            answer = raw_input(
                    "\nWould you like to use this item? "
                    if "any" in item.type else "").lower()
            if answer and "any" in item.type:
                if "y" in answer:
                    self.use_item(name)
                elif "n" not in answer:
                    print ("Please type either 'yes' "
                            "or 'no'.")
                    main.confirm()
                    self.view_inv(item)
        else:
            main.confirm()
        self.view_inv()

    def view_equip(self):
        '''
        Shows currently equipped items and allows for equipping
        of equipment in inventory
        '''

        print "%s\nPress Enter To Go Back\n" %(
                self.list_attribute("equipment"))
        answer = raw_input("\nWhat do you want to check out? ").lower()
        if answer:
            for part, equip in self.equipment.items():
                if equip and (
                        answer == part.replace('_', ' ')
                        or answer == equip.name):
                    break
            else:
                print "\nInvalid choice"
                main.confirm()
                self.view_equip()
                return
            main.clearscreen()
            print ("%s: %s\nPress Enter To Go Back\n" %(
                part.replace('_',' ').capitalize(),
                equip.describe_self()))
            question = "Would you like to equip something here"
            question += ("? " if (not equip or equip.name == "bare")
                    else " or dequip this item? ")
            answer = raw_input(question).lower()
            if answer and "d" not in answer:
                string, equip_list = self.list_attribute(
                        "part equipment in inventory", part)
                print "%s\nPress Enter To Go Back\n" %(string)
                answer = raw_input("\nWhat do you want to "
                        "check out? " if equip_list else ""
                        ).lower()
                if answer and answer in equip_list:
                    main.clearscreen()
                    from equipment import Equipment
                    equip = Equipment(answer)
                    print ("%s\nPress Enter To Go Back\n" %(
                        equip.describe_self()))
                    answer = raw_input("\nDo you want to equip this? ").lower()
                    if "y" in answer and self.validate_equip(equip.type):
                        self.equip(equip, part)
                        print "\n%s was equipped." %(equip.name)
                        main.confirm()
                    elif "n" not in answer:
                        print "\nInvalid choice"
                        main.confirm()
                elif answer:
                    print "\nInvalid choice"
                    main.confirm()
            elif "d" in answer and self.validate_equip("fist"):
                self.equip(equip, part, True)
                print "\n%s was dequipped." %(equip.name)
                main.confirm()
            elif answer:
                #TODO:Fix this when you fix input validation and menus
                print "Please choose between 'equip' or 'dequip'."
                main.confirm()
            self.view_equip()

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

        main.clearscreen()
        remove_skills = self.validate_skills([weapon_type])
        if remove_skills:
            #warn player
            answer = self.validate_input(
                    prompt = ("If you do this, the following skills "
                    "will be removed:\n\n%s\n\nAre you sure you want to "
                    "do this?(y/n) " %("\n".join(remove_skills))),
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

    def view_skills(self, section = ""):
        '''
        Displays skills and allows for in depth info on each
        skill and the equipping and dequipping of skills
        '''

        global skills
        if not section:
            menu = main.create_menu(
                    prompt = ("Skills", "What do you want to see?"),
                    choices = ("U", "E"),
                    options = ("Unequipped", "Equipped"),
                    enter_option = True
                    )
            answer = self.validate_input(
                    prompt = menu,
                    choices = ("u", "e", ""),
                    invalid_prompt = ("Please type 'u' for"
                        " unequipped or 'e' for equipped")
                    )
            if not answer:
                return
        else:
            answer = section
        gen_prompt = "What do you want to check out?"
        if answer == "u":
            menu, skill_list = self.list_attribute("skills",
                    prompt = (gen_prompt if self.skill_bag else ""))
            choice = self.validate_input(
                prompt = menu,
                choices = [str(x+1) for x in range(len(skill_list))] + [""],
                invalid_prompt = "Invalid input."
                )
            if not choice:
                self.view_skills()
                return
            else:
                skill_name = skill_list[int(choice) - 1]

            main.clearscreen()
            skill = skills.Skill(skill_name)
            prompt = "%s\n\nPress Enter To Go Back\n\n" % skill.describe_self()
            if not self.validate_skills(skill_type = skill.type):
                print prompt + "You cannot equip this TYPE of skill."
                main.confirm()
                self.view_skills(section = "u")
                return
            else:
                answer = self.validate_input(
                        prompt = prompt + "Would you like to equip this skill? ",
                        choices = ("y", "n", ""),
                        invalid_prompt = "Please type 'y' or 'n'."
                        )
            if answer == "y":
                if self.equip_skill(skill.name):
                    print "%s was equipped." % skill.name.capitalize()
                    main.confirm()
                    self.view_skills(section = "u")
                    return
                else:
                    warning = ("\n\nNote: 5 skills is the max amount of skills\n"
                            "you can have equipped. To equip another skill,\n"
                            "you must dequip an equipped skill.\n"
                            )
                    sub_menu, sub_options = self.list_attribute(
                            "equipped skills",
                            prompt = gen_prompt.replace("check out", "replace")
                            )
                    sub_choice = self.validate_input(
                        prompt = sub_menu + warning,
                        choices = [str(x+1) for x in range(len(sub_options))] + [""],
                        invalid_prompt = "Invalid input."
                        )
                    if not sub_choice:
                        self.view_skills(section = "u")
                        return
                    else:
                        skill_name = sub_options[int(sub_choice) - 1]
                    re_skill = skills.Skill(skill_name)
                    prompt = "%s\n\nPress Enter To Go Back\n\n" % re_skill.describe_self()
                    answer = self.validate_input(
                            prompt = prompt + "Would you like to replace this skill? ",
                            choices = ("y", "n", ""),
                            invalid_prompt = "Please type 'y' or 'n'."
                            )
                    if answer == 'y':
                        self.equip_skill(re_skill.name, True)
                        self.equip_skill(skill.name)
                        print ("\n%s was dequiped and %s was equipped."
                                %(re_skill.name, skill.name))
                        main.confirm()
                    self.view_skills(section = "u")
            else:
                self.view_skills(section = "u")
                return
        else:
            menu, options = self.list_attribute("equipped skills",
                    prompt = (gen_prompt if self.skills else ""))
            choice = self.validate_input(
                    prompt = menu,
                    choices = ([str(x+1) for x in range(len(options))]
                            + [""]),
                    invalid_prompt = "\nInvalid choice."
                    )
            if not choice:
                self.view_skills()
                return
            try:
                skill_name = options[int(choice) - 1]
                skill = skills.Skill(skill_name)
            except KeyError:
                skill_name = ""
            if skill_name:
                while 1:
                    choice = self.validate_input(
                            prompt = ("%s\n\nPress Enter To Go Back\n\n"
                                "Would you like to equip something else here"
                                " or dequip this skill? " % skill.describe_self()),
                            choices = ("equip", "dequip", ""),
                            invalid_prompt = ("Please type either 'equip'"
                                " or 'dequip'.")
                            )
                    if not choice:
                        self.view_skills(section = 'e')
                        return
                    elif choice == "equip":
                        answer = ""
                        while 1:
                            sub_menu, sub_options = self.list_attribute(
                                    "skills",
                                    prompt = gen_prompt)
                            sub_choice = self.validate_input(
                                    prompt = sub_menu,
                                    choices = [str(x+1) for x in
                                        range(len(sub_options))] + [""],
                                    invalid_prompt = "\nInvalid choice."
                                    )
                            if sub_choice:
                                re_skill = skills.Skill(sub_options[
                                    int(sub_choice) - 1])
                                main.clearscreen()
                                prompt = ("%s\n\nPress Enter To Go Back\n\n"
                                        % re_skill.describe_self())
                                if not self.validate_skills(skill_type = re_skill.type):
                                    print prompt + "You cannot equip this TYPE of skill."
                                    main.confirm()
                                else:
                                    answer = self.validate_input(
                                            prompt = (prompt +
                                                "Would you like to equip this skill? "),
                                            choices = ("y", "n", ""),
                                            invalid_prompt = ("Please type either"
                                                " 'y' or 'n'.")
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
                        print "\n%s was dequipped." % skill_name
                        main.confirm()
                        break
                self.view_skills(section = "e")
            else:
                answer = self.validate_input(
                        prompt = ("This is an empty slot\n\n"
                            "Press Enter To Go Back\n\n"
                            "Do you want to equip something here? "),
                        choices = ('y','n',''),
                        invalid_prompt = "Please type either 'y' or 'n'."
                        )
                if answer == 'y':
                    while 1:
                        sub_menu, sub_options = self.list_attribute(
                                "skills",
                                prompt = gen_prompt)
                        sub_choice = self.validate_input(
                                prompt = sub_menu,
                                choices = [str(x+1) for x in
                                    range(len(sub_options))] + [""],
                                invalid_prompt = "Invalid choice."
                                )
                        if sub_choice:
                            skill = skills.Skill(sub_options[int(sub_choice)-1])
                            answer = self.validate_input(
                                    prompt = ("%s\n\nPress Enter To Go Back\n\n"
                                        "Would you like to equip this skill? "
                                        % skill.describe_self()),
                                    choices = ("y", "n", ""),
                                    invalid_prompt = ("Please type either"
                                        " 'y' or 'n'.")
                                    )
                            if answer == 'y':
                                self.equip_skill(skill.name)
                                print "%s was equipped" % skill.name
                                main.confirm()
                        if not sub_choice or answer == 'y':
                            break
                self.view_skills(section = "e")

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

        print ''
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
            print "\n*****DANGER*****\n"
            answer = raw_input("\nYour health is currently at %d, a"
                    "nd you currently have %d potions in your inven"
                    "tory. \nWould you like to use one? " % (health, potions)
                    ).lower()
            if 'y' in answer:
                self.use_item("potion")
            else:
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
