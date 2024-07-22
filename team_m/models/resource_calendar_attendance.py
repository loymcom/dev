from odoo import _, api, fields, models

class ResourceCalendar(models.Model):
    _inherit = "resource.calendar.attendance"

    @api.model
    def _team_m_search(self, team_m_values):
        """ Return search domain """
        values = team_m_values
        return self.search(
            [
                ("calendar_id.name", "=", values["calendar"]),
                ("dayofweek", "=", values["dayofweek"]),
                ("day_period", "=", values["day_period"]),
            ]
        )

    @api.model
    def _team_m_to_odoo(self, team_m_values):
        """ Return odoo values """
        Calendar = self.env["resource.calendar"]
        values = team_m_values
        odoo_values = {
            "calendar_id": Calendar._team_m_search(team_m_values).id,
            "name": values["name"],
            "dayofweek": values["dayofweek"],
            "day_period": values["day_period"],
            "hour_from": values["hour_from"],
            "hour_to": values["hour_to"],
        }
        return odoo_values
