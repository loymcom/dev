from odoo import _, api, fields, models


class ResourceGroup(models.Model):
    _inherit = "resource.group"

    # FIXME: Hard-coded for Fredheim
    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        name = self._teamm2odoo_get_value("resource.group")
        if len(name) == 1:
            kwargs |= {
                "name": f"Spania rom {name}",
            }
        return super()._teamm2odoo_search_kwargs(kwargs)
