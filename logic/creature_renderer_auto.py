from bb_renderer import BB_Renderer

from list_builder import List_Builder

class Creature_Renderer_Auto:
    
    ATTRIBUTE_ORDER = ["CON", "STR", "DEX", "INT", "WIL", "PER"]

    BB_HELPER = BB_Renderer()
    
    def __init__(self, yaml_input, autolinker):
        self.yaml_input = yaml_input
        self.autolinker = autolinker
        self.list_builder = List_Builder(autolinker)
        self.actions = self.yaml_input.get("actions").get("active")
        self.passives = self.yaml_input.get("actions").get("passive")
        self.tags = self.yaml_input.get("info").get("tags", [])
        self.mods = self.get_attr_mods()
        self.prof = self.get_proficiencies()


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
    
    def get_proficiencies(self):
        for p in self.passives:
            if p.get("name") == "Proficiencies":
                return p.get("effect")
        return []
            
    def format_actions(self):
        result = ""
        manual_list = []
        auto_list = []
        for a in self.actions:
            if a.get("auto", False):
                auto_list.append(a)
            else:
                manual_list.append(a)
        if len(auto_list):
            for a in auto_list:
                result += self.calc_action(a)
        if len(manual_list):
            result += self.list_builder.build_list_with_subitems(manual_list, supercontainer = "creature-action", list_type="br")
        return result
            
    def calc_action(self, a):
        atype = a.get("type", False)
        auto = a.get("auto")
        if isinstance(auto, list):
            hit = self.format_spell_hit(a)
            dmg = self.format_spell_damage(a)
        else:
            hit = self.format_weapon_hit(a)
            dmg = self.format_weapon_damage(a)
        effect = a.get("effect", False)
        cost = a.get("cost", False)
        save = a.get("save", False)
        skills = a.get("skills", False)
        perks = a.get("perks", False)
        result = "[container:creature-action-container]"
        result += f"[section:creature-action-name]{a.get('name')}[/section]"
        if atype:
            result += f"[br][section:creature-action-type]{atype}[/section]"
        if hit:
            result += f"[container:subitem][section:clr-hit]{hit}[/section][/container]"
        if dmg:
            result += f"[container:subitem][section:clr-roll]{dmg}[/section][/container]"
        if effect:
            for e in effect:
                result += f"[container:subitem]{e}[/container]"
        if save:
            result += f"[container:subitem]{save}[/container]"
        if cost:
            result += f"[container:subitem]{cost}[/container]"
        if skills:
            result += f"[container:subitem]{self.list_builder.build_list(skills, to_link ='skill', list_type='comma')}[/container]"
        if perks:
            result += f"[container:subitem]{self.list_builder.build_list(perks, to_link ='perk', list_type='comma')}[/container]"
        return result + "[/container]"
    
    def format_weapon_hit(self, a):
        prof = self.get_prof_value(a)
        equiv = a.get("auto")
        adata = self.autolinker.fetch_weapon_data(equiv)
        hval = int(int(self.mods.get("DEX")) * float(adata.get("hr")) + prof)
        bval = self.get_action_block_value(adata, prof)
        result = f"Hit+{hval}"
        if bval:
            bstr = int(self.mods.get("CON")) + int(self.mods.get("STR"))
            if a.get("shield", False):
                bstr += 2
            elif adata.get("type") == "Shield":
                for t in adata.get("tags"):
                    if t[0] == "Shield":
                        bstr += t[1] + int(a.get("q", 0))
            if adata.get("type") == "Primitive":
                if not adata.get("block", False):
                    bstr = int(bstr/2)
            result += f", Block+{bval+self.get_reflex_bonus()}|{bstr}"
        return result
    
    def format_weapon_damage(self, a):
        equiv = a.get("auto")
        adata = self.autolinker.fetch_weapon_data(equiv)
        qval = int(a.get("q", 0))
        dr_bonus = int(int(self.mods.get("STR")) * float(adata.get("dr")))
        dmg = adata.get("damage")
        total = dr_bonus+qval
        if total:
            return f"{dmg[0]}+{total} {dmg[1]}"
        else:
            return f"{dmg[0]} {dmg[1]}"
    
    def format_spell_hit(self, a):
        prof = self.get_prof_value(a)
        auto_type = a.get("auto")
        spell_type = auto_type[0]
        spell_attr = auto_type[1]
        if isinstance(spell_attr, list):
            attr_bonus = 0
            for a in spell_attr:
                attr_bonus += int(self.mods.get(a))
        else:
            attr_bonus = int(self.mods.get(spell_attr))
        if spell_type in ["PA", "SA"]:
            return f"Hit+{attr_bonus+prof}"
        elif spell_type == "SD":
            return f"[section:clr-sd]SD+{attr_bonus+prof}[/section]"
        elif spell_type == "DC":
            return f"[section:clr-dc]DC {10+attr_bonus+prof}[/section]"
        return "SPELL HIT ERROR"
    
    def format_spell_damage(self, a):
        prof = self.get_prof_value(a)
        if a.get("aoe", False):
            prof = int(prof/2)
        dmg = a.get("damage", False)
        if dmg:
            if prof:
                return f"{dmg[0]}+{prof} {dmg[1]}"
            else:
                return f"{dmg[0]} {dmg[1]}"
        else:
            return False

            
    def get_prof_value(self, a):
        result = 0
        prof_name = "None"
        equiv = a.get("auto", False)
        if not isinstance(equiv, list):
            adata = self.autolinker.fetch_weapon_data(equiv)
            prof_name = adata.get("type")
        else:
            prof_name = a.get("prof")
        for p in self.prof:
            if p[0] == prof_name:
                result = p[1]
        if not result:
            for p in self.prof:
                if p[0] == "Universal":
                    result = p[1]
        return result
    
    def get_reflex_bonus(self):
        for t in self.tags:
            if t[0] == "Reflexes":
                return t[1]
        return 0
    
    def get_action_block_value(self, adata, prof):
        wtype = adata.get("type", False)
        wtags = adata.get("tags", [])
        if wtype in [False,"Bow","Crossbow","Sling","Thrown"]:
            return False
        if "No Block" in wtags:
            return False
        return int(self.mods.get("CON")) + int(self.mods.get("STR")) + prof