from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        if teamm_values.get("room sharing", "").lower() in ("private", "share room"):
            if teamm_values["room sharing"] == "Share room":
                operator = "ilike"
            else:
                operator = "not ilike"
            domain = [
                ("name", "ilike", teamm_values["room standard"]),
                ("name", "ilike", self.env["teamm"].ROOM[teamm_values["room size"]]),
                ("name", operator, "shared"),
            ]
            return self.search(domain)
        else:
            return super()._teamm2odoo_search(teamm_values)
