from odoo import _, api, fields, models

class ResourceCalendar(models.Model):
    _inherit = "resource.calendar.attendance"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        values = teamm_values
        return self.search(
            [
                ("calendar_id.name", "=", values["calendar"]),
                ("dayofweek", "=", values["dayofweek"]),
                ("day_period", "=", values["day_period"]),
            ]
        )

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Calendar = self.env["resource.calendar"]
        values = teamm_values
        odoo_values = {
            "calendar_id": Calendar._teamm2odoo_search(teamm_values).id,
            "name": values["name"],
            "dayofweek": values["dayofweek"],
            "day_period": values["day_period"],
            "hour_from": values["hour_from"],
            "hour_to": values["hour_to"],
        }
        return odoo_values
