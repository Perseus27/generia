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
    
    def format_weapons(self):
        weapons = self.yaml_input.get("inventory").get("weapons")
        weapons_autocalc_data = []
        weapons_manual = []
        result = ""
        for w in weapons:
            wdata = self.autolinker.fetch_weapon_data(w.get("name"))
            if wdata:
                weapons_autocalc_data.append([wdata, w])
            else:
                weapons_manual.append(w)
        if len(weapons_autocalc_data):
            result += "[ul]"
            for x in weapons_autocalc_data:
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
        result += f"{weapon.get('name')}{qstring}"
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
            return int(result/2)
        return result
