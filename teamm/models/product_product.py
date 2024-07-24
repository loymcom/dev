from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        if not teamm_values.get("room sharing", ""):
            return super()._teamm2odoo_search(teamm_values)
        elif not teamm_values["room sharing"].lower() in ("private", "share room"):
            raise UserError("Room sharing should be private or share room.")
        
        share_operator, share_value = self.env["teamm"].room_sharing(teamm_values)

        # TODO: simplify by using "room description"
        domain = [
            ("name", "ilike", teamm_values["program"]),
            (
                "product_template_variant_value_ids.product_attribute_value_id.name",
                "ilike",
                teamm_values["room standard"],
            ),
            (
                "product_template_variant_value_ids.product_attribute_value_id.name",
                "ilike",
                self.env["teamm"].ROOM[teamm_values["room size"]],
            ),
            (
                "product_template_variant_value_ids.product_attribute_value_id.name",
                share_operator,
                share_value,
            ),
        ]
        return self.search(domain)
