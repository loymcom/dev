manifest = """
{{
    "name": "{shortdesc}",
    "data": [{data}
        "views/menus.xml",
    ],
    "depends": [
        "base",
    ],
    "version": "1.0",
}}
"""

manifest_data = """\n        "views/{model}_views.xml","""

# MODEL

init = "from . import {model}\n"

model = """from odoo import api, fields, models

class {classname}(models.Model):
    _name = "{modelname}"

{fields_py}
"""

model_field = """\n    {field} = fields.{ttype}({attrs}\n    )"""

model_field_attr = "\n        {attr}={value},"
model_field_attr_quote = """\n        {attr}="{value}","""

# ACCESS

access_header = "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink,perm_export"
access_line = "access_{_model_},{model},model_{_model_},{group_extid},1,1,1,1,1"

# XML

xml = """
<?xml version="1.0" encoding="utf-8" ?>
<odoo>{content}
</odoo>
"""

view = """
    <record if="{_model_}_view_{view}" model="ir.ui.view">
        <field name="name">{model}.view.form</field>
        <field name="model">{model}</field>
        <field name="arch" type="xml">
            <{view}>{content}
            </{view}>
        </field>
    </record>
"""

sheet = """
                <sheet>{content}
                </sheet>
"""

group = """
                    <group>{content}
                    </group>
"""

field = """
                        <field name="{field}" {extra}/>
"""

action = """
    <record id="{_model_}_action" model="ir.actions.act_window">
        <field name="name">{model} action</field>
        <field name="res_model">{model}</field>
        <field name="view_mode">tree,form</field>
    </record>
"""

menu_main = """
    <menuitem
        id="{_module_}_main_menu"
        parent="{parent_menu_extid}"
        string="{module_desc}"
    />
"""

menu_item = """
    <menuitem
        id="{_model_}_menu"
        action="{_model_}_action"
        parent="{_module_}_main_menu"
        string="{model_desc}"
        sequence="{sequence}"
    />
"""

