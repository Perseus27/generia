from bb_renderer import BB_Renderer

from list_builder import List_Builder

class Character_Renderer_Auto:
    
    ATTRIBUTE_ORDER = ["CON", "STR", "DEX", "INT", "WIL", "PER"]

    BB_HELPER = BB_Renderer()
    
    def __init__(self, yaml_input, autolinker):
        self.yaml_input = yaml_input
        self.autolinker = autolinker
        self.list_builder = List_Builder(autolinker)
        self.mods = self.get_attr_mods()


    def get_attr_mods(self):
        attr = self.yaml_input.get("attributes")
        a = [attr.get(x) for x in self.ATTRIBUTE_ORDER]
        mod_list = []
        for x in a:
            if len(x) > 2:
                mod = int(x[1])+int(x[2])
            else:
                mod = int(x[1])
            mod_list.append(mod)
        return {
            "CON" : mod_list[0],
            "STR" : mod_list[1],
            "DEX" : mod_list[2],
            "INT" : mod_list[3],
            "WIL" : mod_list[4],
            "PER" : mod_list[5]
        }

    def format_armor(self):
        armor = self.yaml_input.get("inventory").get("armor")
        result = "[ul]"
        for a in armor:
            result += "[li]"
            name = a.get("name")
            disp_name = a.get("disp", False)
            subname = False
            if disp_name:
                subname = name
                name = disp_name
            qval = int(a.get("q", 0))
            qstr = ""
            if qval > 0:
                qstr = f"+{qval}"
            elif qval < 0:
                qstr = f"-{qval}"
            result += f"{name}{qstr}"
            if subname:
                result += f"[container:subitem][section:subname]{subname}[/section][/container]"
            ench = a.get("enchantments", False)
            curses = a.get("curses", False)
            if ench:
                result += f"[container:subitem]{self.list_builder.build_list(ench, to_link ='ench', list_type='comma', color_id='clr-ench')}[/container]"
            if curses:
                result += f"[container:subitem]{self.list_builder.build_list(curses, to_link ='ench', list_type='comma', color_id='clr-curse')}[/container]"
            result += "[/li]"
        return result + "[/ul]"

    def get_armor_values(self):
        armor = self.yaml_input.get("inventory").get("armor")
        head = 0
        head_bonus = 0
        torso = 0
        torso_bonus = 0
        arms = 0
        arms_bonus = 0
        legs = 0
        legs_bonus = 0
        md = 0
        md_bonus = 0
        er = 0
        for a in armor:
            name = a.get("name")
            ench = a.get("enchantments", False)
            qval = int(a.get("q", 0))
            av_bonus = 0
            # get enchantment values
            if ench:
                for e in ench:
                    if e == "AV+1":
                        av_bonus += 1
                    elif e == "AV+2":
                        av_bonus += 2
                    elif e == "AV+3":
                        av_bonus += 3
                    elif e == "MD+1":
                        md_bonus += 1
                    elif e == "MD+2":
                        md_bonus += 2
                    elif e == "MD+3":
                        md_bonus += 3
            # check if trinket, quit if true to skip expensive autolinker call
            if name in ["Amulet","Ring"]:
                md += qval
                continue
            adata = self.autolinker.fetch_armor_data(name)
            if adata:
                atype = adata.get("type", False)
                av = int(adata.get("av"))
                if atype == "Head":
                    head += av + qval
                    head_bonus += av_bonus
                elif atype == "Torso":
                    torso += av + qval
                    torso_bonus += av_bonus
                elif atype == "Arms":
                    arms += av + qval
                    arms_bonus += av_bonus
                elif atype == "Legs":
                    legs += av + qval
                    legs_bonus += av_bonus
                # check encumbrance rating
                er_pre = int(adata.get("er", 0))
                if er_pre < 0:
                    #check if Armor Familiarity I or II
                    cperks = self.yaml_input.get("perks").get("combat")
                    er_perk_bonus = 0
                    if "Armor Familiarity I" in cperks:
                        er_perk_bonus = 1
                    if "Armor Familiarity II" in cperks:
                        er_perk_bonus = 2
                    er_pre += er_perk_bonus
                    if er_pre > 0:
                        er_pre = 0
                er += er_pre
        # check if unarmored, apply ER bonus
        for x in [head, torso, arms, legs]:
            if x == 0:
                er += 2
        return {
            "head":     [head, head_bonus],
            "torso":    [torso, torso_bonus],
            "arms":     [arms, arms_bonus],
            "legs":     [legs, legs_bonus],
            "md":       [md, md_bonus],
            "er":       er
        }

    def format_weapons(self):
        weapons = self.yaml_input.get("inventory").get("weapons")
        weapons_autocalc = []
        weapons_manual = []
        result = ""
        for w in weapons:
            wdata = self.autolinker.fetch_weapon_data(w.get("name"))
            if wdata:
                weapons_autocalc.append([wdata, w])
            else:
                weapons_manual.append(w)
        if len(weapons_autocalc):
            result += "[ul]"
            for x in weapons_autocalc:
                result += self.calc_weapon(x)
            result += "[/ul]"
        if len(weapons_manual):
            result += self.list_builder.build_list_with_subitems(weapons_manual)
        return result

    def calc_weapon(self, weapon_full):
        weapon = weapon_full[0]
        qvalue = int(weapon_full[1].get("q", 0))
        proficiency = self.get_weapon_proficiency(weapon)
        qstring = ""
        if qvalue > 0:
            qstring = f"+{qvalue}"
        elif qvalue < 0:
            qstring = f"-{qvalue}"
        dmg_string = self.get_weapon_damage_string(weapon, qvalue)
        hit_value = self.get_weapon_hit_value(weapon, proficiency)
        block_value = self.get_weapon_block_value(weapon, proficiency)
        if block_value:
            block_strength = self.get_weapon_block_strength(weapon, qvalue)
        ench = weapon_full[1].get("enchantments", False)
        curses = weapon_full[1].get("curses", False)
        # Open
        result = "[li]"
        # Name+Quality
        name = weapon_full[1].get('name')
        subname = False
        disp_name = weapon_full[1].get('disp', False)
        if disp_name:
            subname = name
            name = disp_name
        result += f"{name}{qstring}"
        if subname:
            result += f"[container:subitem][section:subname]{subname}[/section][/container]"
        # Hit+X, Block+Y|Z
        result += "[container:subitem][section:clr-hit]"
        if block_value:
            result += f"Hit+{hit_value}, Block+{block_value}|{block_strength}"
        else:
            result += f"Hit+{hit_value}"
        result += "[/section][/container]"
        # Damage
        result += f"[container:subitem][section:clr-roll]{dmg_string}[/section][/container]"
        # Enchantments
        if ench:
            result += f"[container:subitem]{self.list_builder.build_list(ench, to_link ='ench', list_type='comma', color_id='clr-ench')}[/container]"
        # Curses
        if curses:
            result += f"[container:subitem]{self.list_builder.build_list(curses, to_link ='ench', list_type='comma', color_id='clr-curse')}[/container]"
        # Finalize
        result += "[/li]"
        return result

    def get_weapon_proficiency(self, weapon):
        result = 0
        for x in self.yaml_input.get("proficiencies").get("weapons"):
            if isinstance(x, list):
                if x[0] == weapon.get("type", False):
                    result = x[1]
        return result
    
    def get_weapon_damage_string(self, weapon, qvalue):
        wdamage = weapon.get("damage")
        if weapon.get("type") == "Shield":
            qvalue = 0
        dmg_bonus = int(int(self.mods.get("STR")) * float(weapon.get("dr")) + qvalue)
        bonus = ""
        if dmg_bonus > 0:
            bonus = f"+{dmg_bonus}"
        elif dmg_bonus < 0:
            bonus = f"-{dmg_bonus}"
        return f"{wdamage[0]}{bonus} {wdamage[1]}"

    def get_weapon_hit_value(self, weapon, prof):
        return int(int(self.mods.get("DEX")) * float(weapon.get("hr")) + prof)
    
    def get_weapon_block_value(self, weapon, prof):
        wtype = weapon.get("type", False)
        if wtype in [False,"Bow","Crossbow","Sling","Thrown"]:
            return False
        return int(self.mods.get("CON")) + int(self.mods.get("STR")) + prof
    
    def get_weapon_block_strength(self, weapon, qvalue):
        wtype = weapon.get("type")
        shield_bonus = 0
        if wtype == "Shield":
            for t in weapon.get("tags"):
                if t[0] == "Shield":
                    shield_bonus = t[1]
            shield_bonus += qvalue
        result = int(self.mods.get("CON")) + int(self.mods.get("STR")) + shield_bonus
        if wtype == "Primitive":
            if not weapon.get("block", False):
                return int(result/2)
        return result


    def format_spells(self):
        spells = self.yaml_input.get("actions").get("spells")
        spells_autocalc = []
        spells_manual = []
        result = ""
        for s in spells:
            sdata = self.autolinker.fetch_spell_data_if_auto(s)
            if sdata:
                spells_autocalc.append([sdata, s])
            else:
                spells_manual.append(s)
        if len(spells_autocalc):
            result += "[ul]"
            for x in spells_autocalc:
                result += self.calc_spell(x)
            result += "[/ul]"
        if len(spells_manual):
            result += self.list_builder.build_list(spells_manual, to_link="spell")
        return result
    
    def calc_spell(self, spell_full):
        display_name = spell_full[1]
        linked_name = f"[url:{self.autolinker.link_spell(display_name)}]{display_name}[/url]"
        return f"[li]{linked_name} {self.get_spell_hit_string(spell_full[0], self.get_spell_proficiency(spell_full[0]))}[/li]"

    def get_spell_proficiency(self, spell):
        result = 0
        for x in self.yaml_input.get("proficiencies").get("magic"):
            if isinstance(x, list):
                if x[0] in spell.get("tags"):
                    result = x[1]
        return result

    def get_spell_hit_string(self, spell, prof):
        atype = spell.get("auto_type")
        if len(atype) < 3:
            mod_val = int(self.mods.get(atype[1]))
        else:
            mod_val = int(self.mods.get(atype[1])) + int(self.mods.get(atype[2]))
        if atype[0] in ["DC", "DC+"]:
            if atype[0] == "DC":
                plus = ""
            else:
                plus = "+"
            return f"[section:clr-dc]{10+mod_val+prof}{plus}[/section]"
        else:
            return f"[section:clr-{atype[0].lower()}]+{mod_val+prof}[/section]"