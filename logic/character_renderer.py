from bb_renderer import BB_Renderer

from list_builder import List_Builder

from character_renderer_auto import Character_Renderer_Auto

class Character_Renderer:
    
    ATTRIBUTE_ORDER = ["CON", "STR", "DEX", "INT", "WIL", "PER"]
    VALUE_ORDER = ["EN", "MP", "MPR", "WL", "WT", "TN", "MS"]
    ARMOR_ORDER = ["head", "torso", "arms", "legs", "md"]
    DEFAULT_HITZONES = ["Head", "Torso", "Arms", "Legs"]

    BB_HELPER = BB_Renderer()
    
    def __init__(self, yaml_input, autolinker):
        self.yaml_input = yaml_input
        self.autolinker = autolinker
        self.list_builder = List_Builder(autolinker)
        self.auto = Character_Renderer_Auto(yaml_input, autolinker)


    def get_output(self):
        return self.format_to_html()

    def format_attributes(self):
        all_attributes = self.yaml_input.get("attributes")
        a = [all_attributes.get(x) for x in self.ATTRIBUTE_ORDER]
        for x in a:
            if len(x) > 2:
                if x[2] >= 0:
                    x[1] = f"[section:clr-bonus]{x[1]+x[2]}[/section]"
                else:
                    x[1] = f"[section:clr-malus]{x[1]+x[2]}[/section]"
        attr_bb = f"""
[table][tr][td][b]CON[/b][/td]
[td]{a[0][0]} [{a[0][1]}][/td]
[/tr]
[tr][td][b]STR[/b][/td]
[td]{a[1][0]} [{a[1][1]}][/td]
[/tr]
[tr][td][b]DEX[/b][/td]
[td]{a[2][0]} [{a[2][1]}][/td]
[/tr]
[tr][td][b]INT[/b][/td]
[td]{a[3][0]} [{a[3][1]}][/td]
[/tr]
[tr][td][b]WIL[/b][/td]
[td]{a[4][0]} [{a[4][1]}][/td]
[/tr]
[tr][td][b]PER[/b][/td]
[td]{a[5][0]} [{a[5][1]}][/td]
[/tr][/table]
        """
        return self.BB_HELPER.process(attr_bb)
    
    def format_values(self):
        all_values = self.yaml_input.get("values", {})
        a = [all_values.get(x) for x in self.VALUE_ORDER]
        values_bb = f"""
[table][tr][td][b]EN[/b][/td]
[td]{a[0]}[/td]
[/tr]
[tr][td][b]MP|R[/b][/td]
[td]{a[1]}|{a[2]}[/td]
[/tr]
[tr][td][b]WL[/b][/td]
[td]{a[3]}[/td]
[/tr]
[tr][td][b]WT[/b][/td]
[td]{a[4]}[/td]
[/tr]
[tr][td][b]TN[/b][/td]
[td]{a[5]}[/td]
[/tr]
[tr][td][b]MS[/b][/td]
[td]{a[6]}[/td]
[/tr][/table]
        """
        return self.BB_HELPER.process(values_bb)
    
    def format_armor(self):
        hit_zones = self.yaml_input.get("custom-hitzones", self.DEFAULT_HITZONES)
        armor_bonuses = self.yaml_input.get("armor")
        armor_values = self.auto.get_armor_values()
        h = armor_values.get("head")
        t = armor_values.get("torso")
        a = armor_values.get("arms")
        l = armor_values.get("legs")
        m = armor_values.get("md")
        er = armor_values.get("er") + int(armor_bonuses.get("er"))
        head = h[0] + int(armor_bonuses.get("head"))
        if h[1] > 0:
            head = f"[section:clr-bonus]{h[0]+h[1]}[/section]"
        torso = t[0] + int(armor_bonuses.get("torso"))
        if t[1] > 0:
            torso = f"[section:clr-bonus]{t[0]+t[1]}[/section]"
        arms = a[0] + int(armor_bonuses.get("arms"))
        if a[1] > 0:
            arms = f"[section:clr-bonus]{a[0]+a[1]}[/section]"
        legs = l[0] + int(armor_bonuses.get("legs"))
        if l[1] > 0:
            legs = f"[section:clr-bonus]{l[0]+l[1]}[/section]"
        md = m[0] + int(armor_bonuses.get("md"))
        if m[1] > 0:
            md = f"[section:clr-bonus]{m[0]+m[1]}[/section]"
        if er > 0:
            er = f"[section:clr-bonus]{er}[/section]"
        elif er < 0:
            er = f"[section:clr-malus]{er}[/section]"
        armor_bb = f"""
[table][tr][td][b]{hit_zones[0]}[/b][/td]
[td]{head}[/td]
[/tr]
[tr][td][b]{hit_zones[1]}[/b][/td]
[td]{torso}[/td]
[/tr]
[tr][td][b]{hit_zones[2]}[/b][/td]
[td]{arms}[/td]
[/tr]
[tr][td][b]{hit_zones[3]}[/b][/td]
[td]{legs}[/td]
[/tr]
[tr][td][b]MD[/b][/td]
[td]{md}[/td]
[/tr]
[tr][td][b]ER[/b][/td]
[td]{er}[/td]
[/tr][/table]
        """
        return self.BB_HELPER.process(armor_bb)
    
    def format_info(self):
        i = self.yaml_input.get("info", {})
        species = i.get("species")
        if isinstance(species, list):
            species = self.list_builder.build_list(i.get("species"), to_link="perk", list_type="comma")
        else:
            species = f"[url:{self.autolinker.link_perk(species)}]{species}[/url]"        
        size = i.get("size")
        class_list = self.list_builder.build_list(i.get("classes"), to_link="class", list_type="comma")
        tag_list = self.list_builder.build_list(i.get("tags"), to_link="tag", list_type="commabr")
        info_bb = f"""
[table][tr][td][b]Species:[/b][/td]
[td]{species}[/td]
[/tr]
[tr][td][b]Level:[/b][/td]
[td]{i.get("level")}[/td]
[/tr]
[tr][td][b]Size:[/b][/td]
[td][url:{self.autolinker.link_tag(size)}]{size}[/url][/td]
[/tr]
[/table]
[container:chara-info-container]
[b]Classes:[/b]
[br]{class_list}
[br][b]Tags:[/b]
[br]{tag_list}
[/container]
        """
        return self.BB_HELPER.process(info_bb)
    
    def format_notes(self):
        return self.BB_HELPER.process(self.yaml_input.get("notes"))

    def format_items(self):
        all_items = self.yaml_input.get("inventory")
        #weapons = self.list_builder.build_list_with_subitems(all_items.get("weapons"))
        weapons = self.auto.format_weapons()
        #armor = self.list_builder.build_list_with_subitems(all_items.get("armor"))
        armor = self.auto.format_armor()
        misc = self.list_builder.build_list_with_subitems(all_items.get("misc"))
        items_formatted = {"weapons" : self.BB_HELPER.process(weapons), "armor" : self.BB_HELPER.process(armor), "misc" : self.BB_HELPER.process(misc)}
        return items_formatted

    def format_proficiencies(self):
        all_proficiencies = self.yaml_input.get("proficiencies")
        magic = self.list_builder.build_list(all_proficiencies.get("magic"), prof_list=True)
        weapons = self.list_builder.build_list(all_proficiencies.get("weapons"), prof_list=True)
        civilian = self.list_builder.build_list(all_proficiencies.get("civilian"), prof_list=True)
        proficiencies_formatted = {"magic" : self.BB_HELPER.process(magic), "weapons" : self.BB_HELPER.process(weapons), "civilian" : self.BB_HELPER.process(civilian)}
        return proficiencies_formatted
    
    def format_actions(self):
        all_actions = self.yaml_input.get("actions")
        skills = self.list_builder.build_list(all_actions.get("skills"), to_link="skill", format_exclusives=True)
        #spells = self.list_builder.build_list(all_actions.get("spells"), to_link="spell")
        spells = self.auto.format_spells()
        rituals = self.list_builder.build_list(all_actions.get("rituals"), to_link="spell", format_exclusives=True)
        actions_formatted = {"skills" : self.BB_HELPER.process(skills), "spells" : self.BB_HELPER.process(spells), "rituals" : self.BB_HELPER.process(rituals)}
        return actions_formatted

    def format_perks(self):
        all_perks = self.yaml_input.get("perks")
        special_perks_bb = self.list_builder.build_list(all_perks.get("special"), to_link="perk")
        combat_perks_bb = self.list_builder.build_list(all_perks.get("combat"), to_link="perk", format_exclusives=True)
        magic_perks_bb = self.list_builder.build_list(all_perks.get("magic"), to_link="perk", format_exclusives=True)
        perks_formatted = {"special" : self.BB_HELPER.process(special_perks_bb), "combat" : self.BB_HELPER.process(combat_perks_bb), "magic" : self.BB_HELPER.process(magic_perks_bb)}
        return perks_formatted

    def format_to_html(self):
        item_list = self.format_items()
        prof_list = self.format_proficiencies()
        act_list = self.format_actions()
        perk_list = self.format_perks()
        result = f"""
<div class="chara-block">
    <div class="chara-toprow">
        <h3 id="{self.yaml_input.get("id")}">{self.yaml_input.get("name")}</h3>
    </div>
    <div class="chara-content-head">
        <div class="chara-general">
            <h6>General</h6>
            <div class="chara-value-table">
                <span class="chara-table-title">Attributes</span>
                {self.format_attributes()}
            </div>
            <div class="chara-value-table">
                <span class="chara-table-title">Values</span>
                {self.format_values()}
            </div>
            <div class="chara-value-table">
                <span class="chara-table-title">Armor</span>
                {self.format_armor()}
            </div>
        </div>
        <div class="chara-general">
            <h6>Info</h6>
            <div class="chara-info">
                {self.format_info()}
            </div>
            <div class="chara-notes">
                {self.format_notes()}
            </div>
        </div>
    </div>
    <div class="chara-content-body">
        <div class="chara-content-tile">
            <h6>Inventory</h6>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Weapons</span>
                {item_list.get("weapons")}
            </div>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Armor</span>
                {item_list.get("armor")}
            </div>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Misc.</span>
                {item_list.get("misc")}
            </div>
        </div>
        <div class="chara-content-tile">
            <h6>Actions</h6>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Skills</span>
                {act_list.get("skills")}
            </div>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Spells</span>
                {act_list.get("spells")}
            </div>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Rituals</span>
                {act_list.get("rituals")}
            </div>
        </div>
        <div class="chara-content-tile">
            <h6>Proficiencies</h6>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Weapons</span>
                {prof_list.get("weapons")}
            </div>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Magic</span>
                {prof_list.get("magic")}
            </div>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Civilian</span>
                {prof_list.get("civilian")}
            </div>
        </div>
        <div class="chara-content-tile">
            <h6>Perks</h6>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Special</span>
                {perk_list.get("special")}
            </div>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Combat</span>
                {perk_list.get("combat")}
            </div>
            <div class="chara-content-subtile">
                <span class="chara-subtile-title">Magic</span>
                {perk_list.get("magic")}
            </div>
        </div>
    </div>
</div>
        """
        return result