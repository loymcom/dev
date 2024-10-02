from odoo import _, api, fields, models


class ResourceGroup(models.Model):
    _inherit = "resource.group"

    # FIXME: Hard-coded for Fredheim
    @api.model
    def _teamm2odoo_get_value(self, key):
        value = super()._teamm2odoo_get_value(key)
        if key == "resource.group":
            if len(value) == 1 or value == "Massage room":
                return f"Spania rom {value}"
            else:
                return value
