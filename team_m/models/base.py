from odoo import _, api, fields, models

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _team_m_to_odoo_search(self, team_m_values):
        return self.search([])

    @api.model
    def _team_m_to_odoo_values(self, team_m_values):
        return {}

    @api.model
    def _team_m_to_odoo_after_create(self, record):
        pass
