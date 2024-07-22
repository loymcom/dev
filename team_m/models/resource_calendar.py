from odoo import _, api, fields, models

class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    @api.model
    def _team_m_to_odoo_search(self, team_m_values):
        """ Return search domain """
        values = team_m_values
        domain = [("name", "=", values["calendar"])]
        return self.search(domain)

    @api.model
    def _team_m_to_odoo_values(self, team_m_values):
        """ Return odoo values """
        values = team_m_values
        odoo_values = {
            "name": values["calendar"],
        }
        return odoo_values

    @api.model
    def _team_m_to_odoo_after_create(self, record):
        record.attendance_ids.unlink()
