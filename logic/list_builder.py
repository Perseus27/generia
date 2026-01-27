class List_Builder:
    def __init__(self, autolinker):
        self.autolinker = autolinker


    def build_list(self, input_list, to_link = False, list_type = "ul", color_id=False, class_list=False, prof_list=False, format_exclusives=False): # br, comma, li, commabr
        if not isinstance(input_list, list):
            input_list = [input_list]
        result = ""
        ctag_open = ""
        ctag_close = ""
        if list_type == "ul":
            result += "[ul]"
        first = True
        for i in input_list:
            if i == []:
                continue
            list_flag = False
            if list_type == "ul":
                result += "[li]"
            else:
                if first:
                    first = False
                else:
                    if list_type in ["comma", "commabr"]:
                        result += ", "
                    if list_type in ["br", "commabr"]:
                        result += "[br]"
            if color_id:
                ctag_open = f"[section:{color_id}]"
                ctag_close = f"[/section]"
            if isinstance(i, list):
                first_part = i[0]
                second_part = i[1]
                rest = False
                if len(i) > 2:
                    rest = i[2:]
                i = first_part
                list_flag = True
            if to_link:
                link = self.get_link(i, to_link, format_exclusive=format_exclusives)
                exclusive = False
                if isinstance(link, list):
                    exclusive = link[1]
                    link = link[0]
                if exclusive:
                    result += "[section:disp-exclusive]"
                if link:
                    if list_flag:
                        if class_list:
                            result += f"[url:{link}]{ctag_open}{first_part}{ctag_close}[/url] [i]({ctag_open}{second_part}{ctag_close})[/i]"
                        else:
                            result += f"[url:{link}]{ctag_open}{first_part}{ctag_close}[/url] {ctag_open}{second_part}{ctag_close}"
                        if rest:
                            for x in rest:
                                result += f"[br][section:clr-subitem]{x}[/section]"
                    else:
                        result += f"[url:{link}]{ctag_open}{i}{ctag_close}[/url]"
                else:
                    if list_flag:
                        if class_list:
                            result += f"{ctag_open}{first_part} [i]({second_part}{ctag_close})[/i]"
                        else:
                            result += f"{ctag_open}{first_part} {second_part}{ctag_close}"
                        if rest:
                            for x in rest:
                                result += f"[br][section:clr-subitem]{x}[/section]"
                    else:
                        result += ctag_open+i+ctag_close
                if exclusive:
                    result += "[/section]"
            else:
                if prof_list:
                    if list_flag:
                        result += f"[section:prof-sub]{first_part} {second_part}[/section]"
                    else:
                        result += f"[section:prof-main]{i}[/section]"
                elif class_list:
                    result += f"{ctag_open}{first_part} [i]({second_part}{ctag_close})[/i]"
                else:
                    result += ctag_open+i+ctag_close
            if list_type == "ul":
                result += "[/li]"
        if list_type == "ul":
            result += "[/ul]"
        return result
    
    def build_list_with_subitems(self, input_list, supercontainer = False, list_type="ul"):
        result = ""
        if list_type == "ul":
            result += "[ul]"

        for x in input_list:
            if supercontainer == "creature-action":
                result += "[container:creature-action-container]"

            if list_type == "ul":
                result += "[li]"

            for subitem in x:
                #result+=subitem
                if subitem == "name":
                    if supercontainer == "creature-action":
                        result += "[section:creature-action-name]"+x.get(subitem)+"[/section]"
                    else:
                        result += x.get(subitem)
                elif subitem == "type" and supercontainer == "creature-action":
                    result += "[br][section:creature-action-type]"+x.get(subitem)+"[/section]"
                elif subitem == "damage":
                    result += f"[container:subitem][section:clr-roll]{x.get(subitem)}[/section][/container]"
                elif subitem == "hit":
                    result += f"[container:subitem][section:clr-hit]{x.get(subitem)}[/section][/container]"
                elif subitem == "skills":
                    result += f"[container:subitem]{self.build_list(x.get(subitem), to_link ='skill', list_type='comma')}[/container]"
                elif subitem == "perks":
                    result += f"[container:subitem]{self.build_list(x.get(subitem), to_link ='perk', list_type='comma')}[/container]"
                elif subitem == "enchantments":
                    result += f"[container:subitem]{self.build_list(x.get(subitem), to_link ='ench', list_type='comma', color_id='clr-ench')}[/container]"
                elif subitem == "curses":
                    result += f"[container:subitem]{self.build_list(x.get(subitem), to_link ='ench', list_type='comma', color_id='clr-curse')}[/container]"
                else:
                    y = x.get(subitem)
                    if isinstance(y, list):
                        for z in y:
                            if supercontainer == "creature-action" and x.get("name") == "Proficiencies" and subitem == "effect" and isinstance(z, list):
                                result += f"[container:subitem]{z[0]} [section:clr-value]{z[1]}[/section]"
                                if len(z) == 3:
                                    result += f" ([section:clr-attr]{z[2]}[/section])"
                                result += "[/container]"
                            else:
                                result += f"[container:subitem]{z}[/container]"
                    else:
                        result += f"[container:subitem]{y}[/container]"

            if list_type == "ul":
                result += "[/li]"

            if supercontainer:
                result += "[/container]"

            
        if list_type == "ul":
            result += "[/ul]"
        return result
    


    def get_link(self, s, to_link, format_exclusive=False):
        link = False
        if to_link == "class":
            link = self.autolinker.link_class(s)
        elif to_link == "class-overview":
            link = self.autolinker.link_class(s, overview=True)
        elif to_link == "perk":
            link = self.autolinker.link_perk(s, check_exclusive=format_exclusive)
        elif to_link == "skill":
            link = self.autolinker.link_skill(s, check_exclusive=format_exclusive)
        elif to_link == "spell":
            link = self.autolinker.link_spell(s, check_exclusive=format_exclusive)
        elif to_link == "tag":
            link = self.autolinker.link_tag(s)
        elif to_link == "ench":
            link = self.autolinker.link_ench(s)
        return link