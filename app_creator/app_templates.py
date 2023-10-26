manifest = """
{{
    "name": "{app_title}",
    "data": [{data}
        "views/menus.xml",
        "security/ir.model.access.csv",
    ],
    "depends": [
        "base",
    ],
    "version": "1.0",
}}
"""

manifest_data = """\n        "views/{_model_}_views.xml","""

# MODEL

init = "from . import {_model_}\n"

model = """from odoo import api, fields, models

class {Model}(models.Model):
    _name = "{model}"
{fields_py}
"""

model_field = """\n    {field} = fields.{ttype}({attrs}\n    )"""

model_field_attr = "\n        {attr}={value},"
model_field_attr_quote = """\n        {attr}="{value}","""

# ACCESS

access_header = "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n"
access_line = "access_{_model_},{model},model_{_model_},{group_extid},1,1,1,1\n"

# XML

xml = """<?xml version="1.0" encoding="utf-8" ?>
<odoo>{content}
</odoo>
"""

view = """
    <record id="{_model_}_view_{view}" model="ir.ui.view">
        <field name="name">{model}.view.{view}</field>
        <field name="model">{model}</field>
        <field name="arch" type="xml">
            <{view}>{content}
            </{view}>
        </field>
    </record>"""

sheet = """
                <sheet>{content}
                </sheet>"""

group = """
                    <group>{content}
                    </group>"""

field = """
                        <field name="{field}" {extra}/>"""

action = """
    <record id="{_model_}_action" model="ir.actions.act_window">
        <field name="name">{model_title}</field>
        <field name="res_model">{model}</field>
        <field name="view_mode">tree,form</field>
    </record>"""

menu_main = """
    <menuitem
        id="{app}_main_menu"
        parent="{parent_menu_extid}"
        name="{app_title}"
    />"""

menu_item = """
    <menuitem
        id="{_model_}_menu"
        action="{_model_}_action"
        parent="{app}_main_menu"
        name="{model_title}"
        sequence="{sequence}"
    />"""
