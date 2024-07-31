from odoo import api, fields, models

"""
SEE app_creator2.py AND app_templates.py IN THE MAIN DIRECTORY.

TODO: inherit from view
"""

class App(models.Model):
    _name = "app.app"

    name = fields.Char()
    parent_menu_id = fields.Many2one("ir.ui.menu")
    views = fields.Char()
    csv = fields.Text()

    def action_create_app(self, get_from, how_to_apply):
        pass
        # ext_ids
        # models = self.create_models()
        # fields = self.create_fields()
        # access = self.create_access()
        # views = self.create_views()
        # action = self.create_action()
        # menuitem = self.create_menuitem()

        # TEST OK
        # contact = self.env["x_fredheim.partner"].create({"x_first_name": "action_create_app"})

        # A) In-database deployment x_name
        # B) Create an Odoo module file structure
        # Both need to apply the CSV structure from CSV or db records.
