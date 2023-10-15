import csv
import os
from pprint import pprint

# from app_templates import t_manifest, t_manifest_data
# from app_templates import t_access_header, t_access_line, t_init, t_model
# from app_templates import t_model_field, t_model_field_attr, t_model_field_attr_quote
# from app_templates import t_xml, t_view, t_sheet, t_group, t_field, t_action
# from app_templates import t_menu_main, t_menu_item
import app_templates as t


csv_file = "test.csv"
csv_delimiter = ";"
app_parent_path = ".."


def create_app_main():
    module, menus, models, actions, accesses, fields = csv2lists(csv_file)
    lists2app(module, menus, models, actions, accesses, fields)


def csv2lists(csv_file):
    module = {}
    menus = []
    models = []
    actions = []
    accesses = []
    fields = []
    model_tech = ""

    with open(csv_file) as f:
        reader = csv.DictReader(f, delimiter=csv_delimiter, quotechar='"')
        lines = [d for d in reader]
        for counter, line in enumerate(lines):
            line = line_desc2tech(line)

            if line.get("module.tech"):
                module = {
                    "name": line["module.tech"],
                    "shortdesc": line["module.desc"]
                }
                # menus.append(
                #     {
                #         "name": line["module.desc"],
                #         "parent_id": line.get("module.parent_menu_extid"),
                #         "extid": line["module.desc"] + "_action",
                #     }
                # )

            if line.get("model.tech"):
                model_tech = line["model.tech"]
                models.append(
                    {
                        "model": line["model.tech"],
                        "name": line["model.desc"],
                        "context": {
                            "sequence": counter,
                            "group_extid": (
                                line.get("model.group_extid") or "base.group_user"
                            ),
                        },
                    }
                )
                # menus.append(
                #     {
                #         "name": line["model.desc"],
                #         "action": line["model.tech"],
                #         "sequence": counter,
                #         "parent_id": "{}.{}"
                #     }
                # )
                # actions.append(
                #     {
                #         "name": line["model.desc"],
                #         "res_model": line["model.tech"],
                #         # "view_mode": line.get("model.views") or "tree,form"
                #     }
                # )
                # accesses.append(
                #     {
                #         "name": ["model.tech"],
                #         "group_id": line.get("model.group_extid") or "base.group_user",
                #     }
                # )

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
                        # "field_group": line.get("field_group"),
                    },
                }
            )
    return module, menus, models, actions, accesses, fields


def line_desc2tech(line):
    desc2tech = [
        ("module.desc", "module.tech", "_"),
        ("model.desc", "model.tech", "."),
        # ("model.desc", "model.tech", "_"),
        ("field.desc", "field.tech", "_"),
     ]
    for desc, tech, delimiter in desc2tech:
        if line.get(desc) and not line.get(tech):
            line[tech] = line[desc].replace(" ", delimiter).lower()
    return line


def lists2app(module, menus, models, actions, accesses, fields):

    # DIRECTORIES

    app_path = "{}/{}".format(app_parent_path, module["name"])
    os.makedirs(app_path, exist_ok=True)
    os.makedirs(app_path + "/models", exist_ok=True)
    os.makedirs(app_path + "/security", exist_ok=True)
    os.makedirs(app_path + "/views", exist_ok=True)

    # MANIFEST

    data = [
        t.manifest_data.format(
            model=model["model"].replace(".", "_")
        ) for model in models
    ]
    manifest  = t.manifest.format(
        shortdesc=module["shortdesc"],
        data="".join(data),
    )
    with open(app_path + "/__manifest__.py", "w") as f:
        f.write(manifest)

    # INIT

    with open(app_path + "/__init__.py", "w") as f:
        f.write(t.init.format(model="model"))

    with open(app_path + "/models/__init__.py", "w") as f:
        for model in models:
            f.write(t.init.format(model=model["model"]))

    # MODELS

    for model in models:
        classname = model["model"].title().replace(".", "")
        modelname = model["model"]
        fields_py = get_fields_py(model, fields)

        path = "{}/models/{}.py".format(app_path, model["model"].replace(".", "_"))
        with open(path, "w") as f:
            f.write(t.model.format(
                classname=classname,
                modelname=modelname,
                fields_py=fields_py,
            ))

    # ACCESS

    with open(app_path + "/security/ir.model.access.csv", "w") as f:
        f.write(t.access_header)
        for model in models:
            model_name = model["model"]
            _model_name_ = model_name.replace(".", "_")
            group_extid = model["context"]["group_extid"]
            f.write(t.access_line.format(
                model=model,
                _model_=_model_name_,
                group_extid=group_extid,
            ))
        # for access in accesses:
        #     model = access["name"]
        #     _model_ = model.replace(".", "_")
        #     group_extid = access["group_id"]
        #     f.write(t.access_line.format(
        #         model=model,
        #         _model_=_model_,
        #         group_extid=group_extid,
        #     ))

    # XML

    for model in models:
        model_views_xml = get_model_views_xml(model, fields)
        _model_ = model["model"].replace(".", "_")
        with open(app_path + "/views/" + _model_ + "_views.xml", "w") as f:
            f.write(model_views_xml)

    menus_xml = get_menus_xml(module, models)
    with open(app_path + "/views/menus.xml", "w") as f:
        f.write(menus_xml)


def get_fields_py(model, fields):
    fields_py = []
    for counter, field in enumerate(fields):
        if field["model"] == model["model"]:

            # if counter == 0 or field["context"].get("field_group"):
            #     fields_py.append("\n")

            def do_attr(attr, key, quote=False):
                # attr = python method attribute
                # key = csv column dict key
                # quote = boolean, should the value be inside quotes ("value")?
                if key in field:
                    line = t.model_field_attr_quote if quote else t.model_field_attr
                    attrs_py.append(line.format(
                        attr=attr, value=field[key])
                    )
            attrs_py = []
            do_attr("string", "field_description")
            do_attr("comodel_name", "relation")
            do_attr("groups", "groups")

            fields_py.append(t.model_field.format(
                field=field["name"],
                ttype=field["ttype"].capitalize(),
                attrs=attrs_py,
            ))
    return "".join(fields_py)


def get_model_views_xml(model, fields):
    model_name = model["model"]
    _model_name_ = model_name.replace(".", "_")
    form_fields = []
    tree_fields = []
    search_fields = []
    show = 'optional="show" '

    for field in fields:
        if field["model"] == model["model"]:
            form_fields.append(t.field.format(field=field["name"], extra=""))
            tree_fields.append(t.field.format(field=field["name"], extra=show))
            search_fields.append(t.field.format(field=field["name"], extra=""))

    form_group = t.group.format(content="".join(form_fields))
    form_sheet = t.sheet.format(content=form_group)
    form_view = t.view.format(
        model=model_name,
        _model_=_model_name_,
        view="form",
        content=form_sheet,
    )
    tree_view = t.view.format(
        model=model_name,
        _model_=_model_name_,
        view="tree",
        content="".join(tree_fields),
    )
    search_view = t.view.format(
        model=model_name,
        _model_=_model_name_,
        view="search",
        content="".join(search_fields),
    )
    action = t.action.format(
        model=model_name,
        _model_=_model_name_,
    )
    xml = t.xml.format(
        content=form_view + tree_view + search_view + action
    )
    return xml


def get_menus_xml(module, models):
    menus_xml = []
    module_desc = module["shortdesc"]
    _module_ = module["name"]
    parent_menu_extid = module.get("parent_id")
    menus_xml.append(t.menu_main.format(
        module_desc=module_desc,
        _module_=_module_,
        parent_menu_extid=parent_menu_extid,
    ))

    for model in models:
        menus_xml.append(t.menu_item.format(
            model_desc=model["name"],
            _model_=model["model"].replace(".", "_"),
            _module_=_module_,
            sequence=model["context"]["sequence"],
        ))

    return "".join(menus_xml)


create_app_main()
