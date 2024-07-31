from odoo import _, api, fields, models


class ResourceResource(models.Model):
    _inherit = "resource.resource"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        if teamm_values.get("room size"):
            domain = [("name", "=like", self.env["teamm"].bed_name(teamm_values, 1)[:-2] + " %")]
            return self.search(domain)
        else:
            return super()._teamm2odoo_search(teamm_values)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        TeamM = self.env["teamm"]
        Calendar = self.env["resource.calendar"]
        Category = self.env["resource.category"]

        odoo_values = {
            "name": self._teamm2odoo_names(teamm_values)[0],
            "resource_type": "material",
            "calendar_id": Calendar._teamm2odoo_search(teamm_values).id,
            "category_id": Category._teamm2odoo_search(teamm_values).id,
        }
        beds = teamm_values.get("room size")
        if beds and int(beds) > 0:
            odoo_values = [
                {**odoo_values, "name": TeamM.bed_name(teamm_values, i + 1)}
                for i in range(int(beds))
            ]
        return odoo_values
