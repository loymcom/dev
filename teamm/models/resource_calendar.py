from odoo import _, api, fields, models

class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        values = teamm_values
        domain = [("name", "=", values["calendar"])]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        values = teamm_values
        odoo_values = {
            "name": values["calendar"],
        }
        return odoo_values

    @api.model
    def _teamm2odoo_after_create(self, record):
        record.attendance_ids.unlink()
