import yaml
from pathlib import Path

class Autolinker:

    DATA_DIR = Path.cwd() / "docs" / "data"
    CLASS_DIR = DATA_DIR / "classes"
    PERK_DIR = DATA_DIR / "perks"
    SKILL_DIR = DATA_DIR / "skills"
    SPELL_DIR = DATA_DIR / "spells"
    TAG_DIR = DATA_DIR / "tags"
    ENCH_DIR = DATA_DIR / "enchantments"
    ARMOR_DIR = DATA_DIR / "tables" / "armor"
    WEAPON_DIR = DATA_DIR / "tables" / "weapons"

    def __init__(self):
        self.class_yamls = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(self.CLASS_DIR.rglob("*.yaml"))
        ]
        self.perk_yamls = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(self.PERK_DIR.rglob("*.yaml"))
        ]
        self.skill_yamls = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(self.SKILL_DIR.rglob("*.yaml"))
        ]
        self.spell_yamls = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(self.SPELL_DIR.rglob("*.yaml"))
        ]
        self.tag_yamls = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(self.TAG_DIR.rglob("*.yaml"))
        ]
        self.ench_yamls = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(self.ENCH_DIR.rglob("*.yaml"))
        ]
        self.armor_yamls = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(self.ARMOR_DIR.rglob("*.yaml"))
        ]
        self.weapon_yamls = [
            yaml.safe_load(path.read_text(encoding="utf-8"))
            for path in sorted(self.WEAPON_DIR.rglob("*.yaml"))
        ]
        self.class_index = self._build_index(self.class_yamls, self._class_entry_data)
        self.perk_index = self._build_index(self.perk_yamls, self._perk_entry_data)
        self.skill_index = self._build_index(self.skill_yamls, self._skill_entry_data)
        self.spell_index = self._build_index(self.spell_yamls, self._spell_entry_data)
        self.tag_index = self._build_index(self.tag_yamls, self._tag_entry_data)
        self.ench_index = self._build_index(self.ench_yamls, self._ench_entry_data)
        self.armor_index = self._build_index(self.armor_yamls, self._item_entry_data)
        self.weapon_index = self._build_index(self.weapon_yamls, self._item_entry_data)


    def link_class(self, x, overview=False):
        c = self.class_index.get(self._normalize_key(x))
        if c:
            if overview:
                return f"#{c.get('id')}"
            else:
                return f"{c.get('prefix')}/{c.get('id')}"
        return False
    
    def link_perk(self, x, check_exclusive=False):
        p = self.perk_index.get(self._normalize_key(x))
        if p:
            if check_exclusive:
                return [f"{p['prefix']}#{p['item'].get('id', p['item'].get('name'))}", p["item"].get("exclusive"), False]
            else:
                return f"{p['prefix']}#{p['item'].get('id', p['item'].get('name'))}"
        return False

    def link_skill(self, x, check_exclusive=False):
        i = self.skill_index.get(self._normalize_key(x))
        if i:
            skill_item = i["item"]
            if check_exclusive:
                return [f"{i['prefix']}#{skill_item.get('id', skill_item.get('name'))}", any(tag in ["TIER X", "Tier X"] for tag in skill_item.get("tags", []))]
            else:
                return f"{i['prefix']}#{skill_item.get('id', skill_item.get('name'))}"
        return False

    def link_spell(self, x, check_exclusive=False):
        i = self.spell_index.get(self._normalize_key(x))
        if i:
            spell_item = i["item"]
            if check_exclusive:
                return [f"{i['prefix']}#{spell_item.get('id', spell_item.get('name'))}", any(tag in ["TIER X", "Tier X"] for tag in spell_item.get("tags", []))]
            else:
                return f"{i['prefix']}#{spell_item.get('id', spell_item.get('name'))}"
        return False
    
    def link_tag(self, x):
        p = self.tag_index.get(self._normalize_key(x))
        if p:
            return f"{p['prefix']}#{p['item'].get('id', p['item'].get('name'))}"
        return self.link_ench(x)
    
    def link_ench(self, x):
        p = self.ench_index.get(self._normalize_key(x))
        if p:
            return f"{p['prefix']}#{p['item'].get('id', p['item'].get('name'))}"
        return False
    
    
    def fetch_armor_data(self, x):
        a = self.armor_index.get(self._normalize_key(x))
        if a:
            return a["item"]
        return False

    def fetch_weapon_data(self, x):
        w = self.weapon_index.get(self._normalize_key(x))
        if w:
            return w["item"]
        return False
    
    def fetch_spell_data_if_auto(self, x):
        i = self.spell_index.get(self._normalize_key(x))
        if i:
            spell_item = i["item"]
            if spell_item.get("auto_type", False):
                return spell_item
            return False
        return False
    
    def is_spell_exclusive(self, x):
        for y in self.spell_yamls:
            for subcat in self.get_all_spells_from_file(y):
                for s in subcat:
                    if x == s.get("name") or x in s.get("alias", []):
                        if i.get("auto_type", False):
                            return i

    
    def get_all_perks_from_file(self, f):
        return f.get("content", [])
    
    def get_all_skills_from_file(self, f):
        all = [f.get("offensive", False), 
                  f.get("utility", False), 
                  f.get("reaction", False),
                  f.get("tier2", False),
                  f.get("tier3", False),
                  f.get("content", False)]
        result = [x for x in all if x]
        return result
    
    def get_all_spells_from_file(self, f):
        all = [f.get("offensive", False), 
                  f.get("defensive", False), 
                  f.get("utility", False), 
                  f.get("ritual", False),
                  f.get("exclusive", False)]
        result = [x for x in all if x]
        return result
    
    def get_all_contents_from_file(self, f):
        return f.get("content", [])
    
    def get_all_items_from_file(self, f):
        return f.get("items", [])

    def _normalize_key(self, value):
        if value is None:
            return ""
        return str(value).strip().lower()

    def _iter_names(self, item):
        name = item.get("name")
        if name:
            yield name
        for alias in item.get("alias", []) or []:
            if alias:
                yield alias

    def _build_index(self, docs, entry_builder):
        index = {}
        for doc in docs:
            for name, payload in entry_builder(doc):
                key = self._normalize_key(name)
                if key and key not in index:
                    index[key] = payload
        return index

    def _class_entry_data(self, doc):
        for name in self._iter_names(doc):
            yield name, doc

    def _perk_entry_data(self, doc):
        prefix = doc.get("prefix")
        for perk in self.get_all_perks_from_file(doc):
            payload = {"prefix": prefix, "item": perk}
            for name in self._iter_names(perk):
                yield name, payload

    def _skill_entry_data(self, doc):
        prefix = doc.get("prefix")
        for subcat in self.get_all_skills_from_file(doc):
            for skill in subcat:
                payload = {"prefix": prefix, "item": skill}
                for name in self._iter_names(skill):
                    yield name, payload

    def _spell_entry_data(self, doc):
        prefix = doc.get("prefix")
        for subcat in self.get_all_spells_from_file(doc):
            for spell in subcat:
                payload = {"prefix": prefix, "item": spell}
                for name in self._iter_names(spell):
                    yield name, payload

    def _tag_entry_data(self, doc):
        prefix = doc.get("prefix")
        for item in self.get_all_contents_from_file(doc):
            payload = {"prefix": prefix, "item": item}
            for name in self._iter_names(item):
                yield name, payload

    def _ench_entry_data(self, doc):
        prefix = doc.get("prefix")
        for item in self.get_all_contents_from_file(doc):
            payload = {"prefix": prefix, "item": item}
            for name in self._iter_names(item):
                yield name, payload

    def _item_entry_data(self, doc):
        for item in self.get_all_items_from_file(doc):
            payload = {"item": item}
            for name in self._iter_names(item):
                yield name, payload
    
