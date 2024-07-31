from odoo import _, api, fields, models
from odoo.exceptions import UserError

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _teamm2odoo_names(self, teamm_values):
        if teamm_values.get(self._name):
            return [name.strip() for name in teamm_values[self._name].split(",")]
        else:
            return []

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        return self.search([("name", "in", self._teamm2odoo_names(teamm_values))])

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        return {"name": teamm_values[self._name]}

    @api.model
    def _teamm2odoo_after_create(self, records):
        pass
