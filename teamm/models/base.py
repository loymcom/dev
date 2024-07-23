from odoo import _, api, fields, models

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        return self.search([])

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        return {}

    @api.model
    def _teamm2odoo_after_create(self, record):
        pass
