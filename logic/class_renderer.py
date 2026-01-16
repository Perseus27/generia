from bb_renderer import BB_Renderer

from list_builder import List_Builder

class Class_Renderer:

    BB_HELPER = BB_Renderer()

    def __init__(self, yaml_input, autolinker):
        self.yaml_input = yaml_input
        self.autolinker = autolinker
        self.list_builder = List_Builder(autolinker)

    def get_output_main(self):
        return self.BB_HELPER.process(self.format_class_main(self.yaml_input))

    def get_output_card(self):
        return self.BB_HELPER.process(self.format_class_card(self.yaml_input))
    

    def format_class_main(self,c):
        is_tier1 = c.get("prefix") == "class1"
        caster_info = c.get("spellcaster_info", False)
        alias = c.get("alias", False)
        perks = c.get("perks")
        actions = c.get("actions")
        proficiencies = c.get("proficiencies")
        prof_civilian = proficiencies.get("civilian", False)
        if prof_civilian[0] == []:
            prof_civilian = False
        starter_set = c.get("starter_set", [])
        # class header
        result = f"[container:class-main]"
        result += f"[h1]{c.get('name')}[/h1]"
        # alias?
        if alias:
            result += f"[container:class-main-alias][b]Alias:[/b] {self.list_builder.build_list(alias, list_type='comma')}[/container]"
        # spellcaster info
        if caster_info:
            result += f"[container:class-main-caster-info]{caster_info}[/container]"
        # info
        result += f"[container:class-main-info]"
        ## description
        result += f"[h2]Description[/h2]"
        result += f"[container:class-main-description]{c.get('description')}[/container]"
        ## prerequisites
        result += f"[container:class-main-subinfo]"
        result += f"[h4]Prerequisites[/h4]"
        result += f"{self.list_builder.build_list(c.get('prerequisites'), list_type='comma', to_link='class')}"
        ## subclasses
        result += f"[h4]Subclasses[/h4]"
        result += f"{self.list_builder.build_list(c.get('subclasses'), list_type='comma', to_link='class')}"
        result += f"[/container]"
        # close info
        result += f"[/container]"
        result += f"[hr]"
        # body
        result += f"[container:class-main-body]"
        ## perks
        result += f"[h2]Perks[/h2]"
        result += f"[container:class-main-body-category]"
        ### combat
        result += f"[container:class-main-sub50]"
        result += f"[h4]Combat[/h4]"
        result += f"{self.list_builder.build_list(perks.get('combat'), to_link='perk', class_list=True)}"
        result += "[/container]"
        ### magic
        result += f"[container:class-main-sub50]"
        result += f"[h4]Magic[/h4]"
        result += f"{self.list_builder.build_list(perks.get('magic'), to_link='perk', class_list=True)}"
        result += f"[/container]"
        ## close perks
        result += f"[/container]"
        result += f"[hr]"
        ## actions
        result += f"[h2]Actions[/h2]"
        result += f"[container:class-main-body-category]"
        ### skills
        result += f"[container:class-main-sub50]"
        result += f"[h4]Skills[/h4]"
        result += f"{self.list_builder.build_list(actions.get('skills'), to_link='skill', class_list=True)}"
        result += f"[/container]"
        ### spells
        result += f"[container:class-main-sub50]"
        result += f"[h4]Spells[/h4]"
        result += f"{self.list_builder.build_list(actions.get('spells'), to_link='spell', class_list=True)}"
        result += f"[/container]"
        ## close actions
        result += f"[/container]"
        result += f"[hr]"
        ## proficiencies
        result += f"[h2]Proficiencies[/h2]"
        result += f"[container:class-main-body-category]"
        ### weapon
        if prof_civilian:
            result += f"[container:class-main-sub33]"
        else:
            result += f"[container:class-main-sub50]"
        result += f"[h4]Weapons[/h4]"
        result += f"{self.list_builder.build_list(proficiencies.get('weapons'), class_list=True)}"
        result += f"[/container]"
        ### spellcasting
        if prof_civilian:
            result += f"[container:class-main-sub33]"
        else:
            result += f"[container:class-main-sub50]"
        result += f"[h4]Spellcasting[/h4]"
        result += f"{self.list_builder.build_list(proficiencies.get('magic'), class_list=True)}"
        result += f"[/container]"
        ### civilian?
        if prof_civilian:
            result += f"[container:class-main-sub33]"
            result += f"[h4]Civilian[/h4]"
            result += f"{self.list_builder.build_list(prof_civilian, class_list=True)}"
            result += f"[/container]"
        ## close proficiencies
        result += f"[/container]"
        result += f"[hr]"
        # close body
        result += f"[/container]"
        # STARTER SET ???
        if is_tier1:
            result += f"[hr]"
            result += f"[container:class-main-starter]"
            result += f"[h2]Starter Set[/h2]"
            result += f"{self.list_builder.build_list(starter_set)}"
            result += f"[/container]"
        # close class-main
        result += f"[/container]"
        return result
        

    def format_class_card(self, c):
        cid = c.get("id")
        alias = c.get("alias", False)
        result = f"[container:class-card]"
        # header
        result += f"[container:class-card-header][h2|{cid}][url:{c.get('prefix')}/{cid}]{c.get('name')}[/url][/h2][/container]"
        if alias:
            result += f"[container:class-card-alias][b]Alias:[/b] {self.list_builder.build_list(alias, list_type='comma')}[/container]"
        # body
        result += f"[container:class-card-body]"
        # description
        result += f"[container:class-card-description][h4]Description[/h4]{c.get('description')}[/container]"
        # info
        result += f"[container:class-card-info]"
        # prerequisites
        result += f"[h4]Prerequisites[/h4]{self.list_builder.build_list(c.get('prerequisites'), list_type='comma', to_link='class-overview')}"
        # subclasses
        result += f"[h4]Prerequisites[/h4]{self.list_builder.build_list(c.get('subclasses'), list_type='comma', to_link='class-overview')}"
        # close info
        result += f"[/container]"
        # close body
        result += f"[/container]"
        #close card
        result += f"[/container]"
        return result
    