from odoo import _, api, fields, models

class ResourceResource(models.Model):
    _inherit = "resource.resource"

    @api.model
    def _team_m_to_odoo_search(self, team_m_values):
        values = team_m_values
        domain = [("name", "=like", values["room"] + "%")]
        return self.search(domain)

    @api.model
    def _team_m_to_odoo_values(self, team_m_values):
        Calendar = self.env["resource.calendar"]

        values = team_m_values

        if values["type"] == "Dobbelt":
            odoo_values = [
                {
                    "name": values["room"] + " A",
                    "resource_type": "material",
                    "calendar_id": Calendar._team_m_to_odoo_search(team_m_values).id,
                },
                {
                    "name": values["room"] + " B",
                    "resource_type": "material",
                    "calendar_id": Calendar._team_m_to_odoo_search(team_m_values).id,
                },
            ]
        else:
            odoo_values = {
                "name": values["room"],
                "resource_type": "material",
                "calendar_id": Calendar._team_m_to_odoo_search(team_m_values).id,
            },
        return odoo_values
