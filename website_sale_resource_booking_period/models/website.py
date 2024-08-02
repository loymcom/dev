import pytz
from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    shop_model = fields.Selection(
        selection_add=[("shop.product", "Shop Variant")]
    )

    def _product2pav(self):
        """ From product model, get the relation to product attribute values"""        
        if self.shop_model == "shop.product":
            return "product_template_attribute_value_ids.product_attribute_value_id"

        return super()._product2pav()
