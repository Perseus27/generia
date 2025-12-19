from bb_renderer import BB_Renderer

class Perk_Renderer:

    BB_HELPER = BB_Renderer()
    
    def __init__(self, yaml_input):
        self.yaml_input = yaml_input
        self.html_output = ""


    def get_output(self):
        self.format_to_html()
        return self.html_output
    
    def format_to_html(self):
        self.html_output = self.BB_HELPER.process(self.format_all(self.yaml_input.get("content")))
    
    def format_allOLD(self):
        y = self.yaml_input
        id_ap = y.get("id_appendix")
        x = y.get("is_exclusive", False)
        if x:
            return f"""
[h1|Tier{id_ap}]Tier {id_ap}[/h1]
{self.format_spells_from_category(y.get('exclusive', False))}
            """        
        result = f"""
[h1|Tier{id_ap}]Tier {id_ap}[/h1]
[h2|Offensive{id_ap}]Offensive[/h2]
{self.format_spells_from_category(y.get('offensive', False))}
[h2|Defensive{id_ap}]Defensive[/h2]
{self.format_spells_from_category(y.get('defensive', False))}
[h2|Utility{id_ap}]Utility[/h2]
{self.format_spells_from_category(y.get('utility', False))}
[h2|Ritual{id_ap}]Ritual[/h2]
{self.format_spells_from_category(y.get('ritual', False))}
        """
        return result
    

    def format_all(self, perk_yaml):
        if not perk_yaml:
            return "–"
        result = ""
        for i in perk_yaml:
            if i.get("is_subheader", False):
                result += self.format_subheader(i)
            else:
                result += self.format_perk(i)
        return result

    def format_subheader(self, subheader):
        return f"[h3|{subheader.get('id')}]{subheader.get('name')}[/h3]"

    def format_perk(self, perk):
        ###
        perk_bb = f"[container:perk][h2|{perk.get('id')}]{perk.get('name')}[/h2]"
        # sp cost
        perk_bb += f"[b][i]SP Cost:[/i][/b] {perk.get('sp-cost')}"
        # requirements
        perk_bb += f"[br][b]Requirements:[/b][br]{perk.get('requirements')}"
        # description
        perk_bb += f"[br][b]Description:[/b][br]{perk.get('description')}"
        # end
        perk_bb += f"[/container]"
        return perk_bb

