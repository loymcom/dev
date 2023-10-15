t_manifest = """
{{
    "name": "{module_desc}",
    "data": [{data}
    ],
    "depends": [
        "base",
    ],
    "version": "1.0",
}}
"""

# MODEL

t_model = """
from odoo import api, fields, models

class App(models.Model):
    _name = "app.app"

    name = fields.Char()
"""

# ACCESS

t_access = """
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_hotel_session_group,hotel.session.user,model_hotel_session,hotel.group_hotel_user,1,1,1,1
"""

# XML

t_view_form = """

"""

t_view_tree = """

"""

t_view_search = """

"""

t_action = """

"""

t_menuitem = """

"""

