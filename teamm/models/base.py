from odoo import _, api, fields, models
from odoo.exceptions import UserError

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _teamm2odoo_names(self, teamm_values):
        if teamm_values.get(self._name):
            return teamm_values[self._name].split(",")
        else:
            # raise UserError("_teamm2odoo_names(): field {} is missing.".format(self._name))
            return ""

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        return self.search([("name", "in", self._teamm2odoo_names(teamm_values))])

    @api.model
    def _teamm2odoo_after_create(self, record):
        pass
