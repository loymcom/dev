from odoo import _, api, fields, models

def room_name(teamm_values):
    return "Room {standard} {number}".format(
        standard=teamm_values["standard"].split()[0],
        number=teamm_values["room"],
    )

class ResourceResource(models.Model):
    _inherit = "resource.resource"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        domain = [("name", "=like", room_name(teamm_values) + "%")]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Calendar = self.env["resource.calendar"]

        odoo_values = {
            "name": room_name(teamm_values),
            "resource_type": "material",
            "calendar_id": Calendar._teamm2odoo_search(teamm_values).id,
        }

        if teamm_values["beds"] == "2":
            odoo_values = [
                odoo_values | {"name": odoo_values["name"] + " " + letter}
                for letter in ["A", "B"]
            ]

        return odoo_values
