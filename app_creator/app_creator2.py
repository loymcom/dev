import os
import csv
from collections import defaultdict

from app_templates import t_manifest, t_model, t_access
from app_templates import t_view_form, t_view_tree, t_view_search, t_action, t_menuitem


csv_file = "test.csv"
csv_delimiter = ";"


def main():
    menu, module, model, action, access, field = csv2lists(csv_file)
    lists2app(menu, module, model, action, access, field)


def csv2lists(csv_file):
    menus = []
    modules = []
    models = []
    actions = []
    accesses = []
    fields = []

    with open(csv_file) as fp:
        reader = csv.DictReader(fp, delimiter=csv_delimiter, quotechar='"')
        lines = [d for d in reader]
        for counter, line in enumerate(lines):
            module_tech = ""
            model_tech = ""
            field_group = ""
            line = line_desc2tech(line)

            if line.get("module.tech"):
                module_tech = line["module.tech"]
                modules.append(
                    {
                        "name": line["module.tech"],
                        "shortdesc": line["module.desc"]
                    }
                )
                menus.append(
                    {
                        "name": line["module.desc"],
                        "parent_id": line.get("module.parent_menu_extid"),
                    }
                )

            if line.get("model.tech"):
                model_tech = line["model.tech"]
                models.append(
                    {
                        "model": line["model.tech"],
                        "name": line["model.desc"],
                        "context": {"sequence": counter},
                    }
                )
                menus.append(
                    {
                        "name": line["model.desc"],
                        "action": line["model.tech"],
                        "sequence": counter,
                        "parent_id": module_tech,
                    }
                )
                actions.append(
                    {
                        "name": line["model.desc"],
                        "res_model": line["model.tech"],
                        "view_mode": line.get("model.views") or "tree,form"
                    }
                )
                accesses.append(
                    {
                        "name": ["model.desc"],
                        "model_id": line["model.tech"],
                        "group_id": line.get("model.group_extid") or "base.group_user",
                        "perm_read": True,
                        "perm_write": True,
                        "perm_create": True,
                        "perm_unlink": True,
                        "perm_export": True,
                    }
                )

            if line.get("field_group"):
                field_group = line["field_group"]

            fields.append(
                {
                    "name": line["field.tech"],
                    "field_description": line["field.desc"],
                    "ttype": line["field.type"],
                    "relation": line.get("field.relation"),
                    "groups": line.get("field.group_extid"),
                    "model": model_tech,
                    "context": {
                        "sequence": counter,
                        "field_group": field_group,
                    },
                }
            )

    return menus, modules, models, actions, accesses, fields


def line_desc2tech(line):
    desc2tech = [
        ("module.desc", "module.tech"),
        ("model.desc", "model.tech"),
        ("field.desc", "field.tech"),
     ]
    for desc, tech in desc2tech:
        if line.get(desc) and not line.get(tech):
            line[tech] = line[desc].replace(" ", "_").lower()
    return line


def lists2app(menus, modules, models, actions, accesses, fields):
    # MANIFEST
    data = [
        """\n        "views/{}_views.xml",""".format(
            model["model"].replace(".", "_")
        ) for model in models
    ]
    manifest  = t_manifest.format(
        module_desc=modules[0]["shortdesc"],
        data="".join(data),
    )
    print(manifest)

main()
