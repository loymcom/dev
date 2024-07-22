from odoo import _, api, fields, models

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _team_m_search(self, team_m_values):
        pass

    @api.model
    def _team_m_to_odoo(self, team_m_values):
        pass

    @api.model
    def _team_m_after_create(self, record):
        pass
