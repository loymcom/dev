import csv
import os
from pprint import pprint

import app_templates as t


csv_file = "test.csv"
csv_delimiter = ";"
app_parent_path = ".."

# We say "app" instead of "module".

# model_dot = "model.name"
# model_underscore = "model_name"


def create_app_main():
    app, models, fields = csv2lists(csv_file)
    lists2app(app, models, fields)


def csv2lists(csv_file):
    app = {}
    models = []
    fields = []
    model_dot = ""

    with open(csv_file) as f:
        reader = csv.DictReader(f, delimiter=csv_delimiter, quotechar='"')
        lines = [d for d in reader]
        for counter, line in enumerate(lines):
            line = line_add_defaults(line)

            if line.get("app.name"):
                app = line_filter(line, "app.", [])

            if line.get("model.name"):
                model_dot = line["model.dot"]
                line["model.sequence"] = counter
                models.append(
                    line_filter(line, "model.", [])
                )

            line["field.sequence"] = counter
            line["model.dot"] = model_dot
            fields.append(
                line_filter(line, "field.", ["model.dot"])
            )
    return app, models, fields


def line_add_defaults(line):
    if_first_not_second = [
        ("app.name", "app.underscore", " ", "_"),
        ("model.name", "model.dot", " ", "."),
        ("model.name", "model.underscore", " ", "_"),
        ("field.name", "field.underscore", " ", "_"),
        ("model.name", "model.group_extid", line["model.name"], "base.group_user"),
    ]
    for first, second, replace, with_value in if_first_not_second:
        if line.get(first) and not line.get(second):
            line[second] = line[first].replace(replace, with_value).lower()
    return line


def line_filter(line, prefix, keys):
    result = {}
    for key, value in line.items():
        if key.startswith(prefix) or key in keys:
            result[key] = value
    return result


def lists2app(app, models, fields):

    # DIRECTORIES
    app_path = "{}/{}".format(app_parent_path, app["app.underscore"])
    os.makedirs(app_path, exist_ok=True)
    os.makedirs(app_path + "/models", exist_ok=True)
    os.makedirs(app_path + "/security", exist_ok=True)
    os.makedirs(app_path + "/views", exist_ok=True)

    # MANIFEST

    data = [
        t.manifest_data.format(
            _model_=model["model.underscore"]
        ) for model in models
    ]
    manifest = t.manifest.format(
        app_name=app["app.name"],
        data="".join(data),
    )
    with open(app_path + "/__manifest__.py", "w") as f:
        f.write(manifest)

    # INIT

    with open(app_path + "/__init__.py", "w") as f:
        f.write(t.init.format(_model_="models"))

    with open(app_path + "/models/__init__.py", "w") as f:
        for model in models:
            f.write(t.init.format(_model_=model["model.underscore"]))

    # MODELS

    for model in models:
        path = app_path + "/models/" + model["model.underscore"] + ".py"
        with open(path, "w") as f:
            f.write(t.model.format(
                Model=model["model.dot"].title().replace(".", ""),
                model=model["model.dot"],
                fields_py=get_fields_py(model, fields),
            ))

    # ACCESS

    with open(app_path + "/security/ir.model.access.csv", "w") as f:
        f.write(t.access_header)
        for model in models:
            f.write(t.access_line.format(
                model=model["model.dot"],
                _model_=model["model.underscore"],
                group_extid=model["model.group_extid"],
            ))

    # XML

    for model in models:
        model_views_xml = get_model_views_xml(model, fields)
        path = app_path + "/views/" + model["model.underscore"] + "_views.xml"
        with open(path, "w") as f:
            f.write(model_views_xml)

    menus_xml = get_menus_xml(app, models)
    with open(app_path + "/views/menus.xml", "w") as f:
        f.write(menus_xml)


def get_fields_py(model, fields):
    fields_py = []
    for field in fields:
        if field["model.dot"] == model["model.dot"]:

            def do_attr(attr, key, quote=False):
                # attr = python field attribute
                # key = csv column dict key
                # quote = boolean, should the value be inside quotes ("value")?
                if key in field and field.get(key):
                    line = t.model_field_attr_quote if quote else t.model_field_attr
                    attrs_py.append(line.format(
                        attr=attr, value=field[key])
                    )
            attrs_py = []
            do_attr("string", "field.name", quote=True)
            do_attr("comodel_name", "field.relation", quote=True)
            do_attr("groups", "field.groups", quote=True)

            fields_py.append(t.model_field.format(
                field=field["field.underscore"],
                ttype=field["field.type"].capitalize(),
                attrs="".join(attrs_py),
            ))
    return "".join(fields_py)


def get_model_views_xml(model, fields):
    model_name = model["model.name"]
    model_dot = model["model.dot"]
    model_underscore = model["model.underscore"]
    form_fields = []
    tree_fields = []
    search_fields = []
    show = 'optional="show" '

    for field in fields:
        if field["model.dot"] == model_dot:
            fld_underscore = "field.underscore"
            form_fields.append(t.field.format(field=field[fld_underscore], extra=""))
            tree_fields.append(t.field.format(field=field[fld_underscore], extra=show))
            search_fields.append(t.field.format(field=field[fld_underscore], extra=""))

    form_group = t.group.format(content="".join(form_fields))
    form_sheet = t.sheet.format(content=form_group)
    form_view = t.view.format(
        model=model_dot,
        _model_=model_underscore,
        view="form",
        content=form_sheet,
    )
    tree_view = t.view.format(
        model=model_dot,
        _model_=model_underscore,
        view="tree",
        content="".join(tree_fields),
    )
    search_view = t.view.format(
        model=model_dot,
        _model_=model_underscore,
        view="search",
        content="".join(search_fields),
    )
    action = t.action.format(
        model_name=model_name,
        model=model_dot,
        _model_=model_underscore,
    )
    xml = t.xml.format(
        content=form_view + tree_view + search_view + action
    )
    return xml


def get_menus_xml(app, models):
    menus_xml = []

    menus_xml.append(t.menu_main.format(
        app_name=app["app.name"],
        app=app["app.underscore"],
        parent_menu_extid=app.get("parent_menu_extid", ""),
    ))

    for model in models:
        menus_xml.append(t.menu_item.format(
            app=app["app.underscore"],
            _model_=model["model.underscore"],
            model_name=model["model.name"],
            sequence=model["model.sequence"],
        ))

    return t.xml.format(content="".join(menus_xml))


create_app_main()
