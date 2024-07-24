from odoo import _, api, fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        if teamm_values["resource.booking.type"]:
            domain = [("name", "=like", teamm_values["resource.booking.type"] + "%")]
            return self.search(domain)
        else:
            return super()._teamm2odoo_search(teamm_values)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Calendar = self.env["resource.calendar"]
        odoo_values = {
            "name": teamm_values["resource.booking.type"],
            "duration": 240,
            "slot_duration": 24,
            "resource_calendar_id": Calendar._teamm2odoo_search(teamm_values).id,
            "period_type": teamm_values["period_type"],
        }
        if teamm_values["room size"] == "2":
            odoo_values = [
                odoo_values,
                odoo_values | {"name": odoo_values["name"] + " (shared)"},
            ]
        return odoo_values
