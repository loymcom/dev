from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _teamm2odoo_search(self, teamm_values, discount=None):
        TeamM = self.env["teamm"]
        attr_val = "product_template_variant_value_ids.product_attribute_value_id.name"

        if discount:
            domain = [(attr_val, "=", discount)]
            return self.search(domain)
        elif teamm_values.get("room sharing").lower() in ("private", "share room"):
            share_operator, share_value = TeamM.room_sharing(teamm_values)
            domain = [
                ("name", "ilike", teamm_values["program"]),
                (attr_val, "ilike", teamm_values["room standard"]),
                (attr_val, "ilike", TeamM.ROOM[teamm_values["room size"]]),
                (attr_val, share_operator, share_value),
            ]
            return self.search(domain)
        else:
            return super()._teamm2odoo_search(teamm_values)
