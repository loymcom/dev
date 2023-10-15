import os
import csv
from collections import defaultdict


csv_file = "test.csv"


def main():
    menu, module, model, action, access, field = csv2dicts(csv_file)


def csv2dicts(csv_file):
    menu = defaultdict({"context": {}})
    module = {"context": {}}
    model = defaultdict({"context": {}})
    action = defaultdict({"context": {}})
    access = defaultdict({"context": {}})
    field = defaultdict({"context": {}})

    with open(csv_file) as fp:
        reader = csv.DictReader(fp, delimiter=",", quotechar='"')
        lines = [d for d in reader]
        for counter, line in enumerate(lines):
            line = line_desc2tech(line)

            if line.get("module.tech"):
                module = {
                    "name": line["module.tech"],
                    "shortdesc": line["module.desc"]
                }
                menu[0] = {
                    "name": line["module.desc"],
                    "parent_id": line.get("module.parent_menu_extid"),
                }

            tech = line.get("model.tech")
            if tech:
                model[tech] = {
                    "model": line["model.tech"],
                    "name": line["model.desc"],
                    "context": {"sequence": counter},
                }
                menu[counter] = {
                    "name": line["model.desc"],
                    "action": line["model.tech"],
                    "sequence": counter,
                }
                action[tech] = {
                    "name": line["model.desc"],
                    "res_model": line["model.tech"],
                    "view_mode": line.get("model.views") or "tree,form"
                }
                access[tech] = {
                    "name": ["model.desc"],
                    "model_id": line["model.tech"],
                    "group_id": line.get("model.group_extid") or "base.group_user",
                    "perm_read": True,
                    "perm_write": True,
                    "perm_create": True,
                    "perm_unlink": True,
                    "perm_export": True,
                }


            tech = line.get("field.tech")
            field[tech] = {
                "name": line["field.tech"],
                "field_description": line["field.desc"],
                "ttype": line["field.type"],
                "relation": line.get("field.relation"),
                "groups": line.get("field.group_extid"),
                "context": {"sequence": counter},
            }

    return menu, module, model, action, access, field


def line_desc2tech(line):
    desc2tech = [
        ("module.desc", "module.tech"),
        ("model.desc", "model.tech"),
        ("field.desc", "field.tech"),
     ]
    for desc, tech in desc2tech:
        if not line.get(tech):
            line[tech] = line.get(desc).replace(" ", "_").lower()
    return line
