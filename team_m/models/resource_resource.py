from odoo import _, api, fields, models

def room_name(team_m_values):
    return "Room {standard} {number}".format(
        standard=team_m_values["standard"].split()[0],
        number=team_m_values["room"],
    )

class ResourceResource(models.Model):
    _inherit = "resource.resource"

    @api.model
    def _teamm2odoo_search(self, team_m_values):
        values = team_m_values
        domain = [("name", "=like", room_name(team_m_values) + "%")]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, team_m_values):
        Calendar = self.env["resource.calendar"]

        odoo_values = {
            "name": room_name(team_m_values),
            "resource_type": "material",
            "calendar_id": Calendar._teamm2odoo_search(team_m_values).id,
        }

        if team_m_values["type"] == "Dobbelt":
            odoo_values = [
                odoo_values | {"name": odoo_values["name"] + " " + letter}
                for letter in ["A", "B"]
            ]

        return odoo_values
