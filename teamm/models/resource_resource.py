from odoo import _, api, fields, models


class ResourceResource(models.Model):
    _inherit = "resource.resource"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        if teamm_values.get("room size"):
            domain = [("name", "=like", self.env["teamm"].room_name(teamm_values) + "%")]
            return self.search(domain)
        else:
            return super()._teamm2odoo_search(teamm_values)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Calendar = self.env["resource.calendar"]

        odoo_values = {
            "name": self._teamm2odoo_names(teamm_values)[0],
            "resource_type": "material",
            "calendar_id": Calendar._teamm2odoo_search(teamm_values).id,
        }
        if teamm_values["room size"]:
            odoo_values["name"] = self.env["teamm"].room_name(teamm_values)

        if teamm_values["room size"] == "2":
            odoo_values = [
                odoo_values | {"name": odoo_values["name"] + " " + letter}
                for letter in ["A", "B"]
            ]

        return odoo_values
