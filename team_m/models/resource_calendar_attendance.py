from odoo import _, api, fields, models

class ResourceCalendar(models.Model):
    _inherit = "resource.calendar.attendance"

    @api.model
    def _teamm2odoo_search(self, team_m_values):
        values = team_m_values
        return self.search(
            [
                ("calendar_id.name", "=", values["calendar"]),
                ("dayofweek", "=", values["dayofweek"]),
                ("day_period", "=", values["day_period"]),
            ]
        )

    @api.model
    def _teamm2odoo_values(self, team_m_values):
        Calendar = self.env["resource.calendar"]
        values = team_m_values
        odoo_values = {
            "calendar_id": Calendar._teamm2odoo_search(team_m_values).id,
            "name": values["name"],
            "dayofweek": values["dayofweek"],
            "day_period": values["day_period"],
            "hour_from": values["hour_from"],
            "hour_to": values["hour_to"],
        }
        return odoo_values
