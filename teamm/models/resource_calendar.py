from odoo import _, api, fields, models


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    @api.model
    def _teamm2odoo_after_create(self):
        self.attendance_ids.unlink()
