from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    shop_model = fields.Selection(
        selection_add=[("event.booking.combination", "Shop Variant")]
    )

    def _product2pav(self):
        """ From product model, get the relation to product attribute values"""        
        if self.shop_model == "event.booking.combination":
            return "product_template_attribute_value_ids.product_attribute_value_id"

        return super()._product2pav()
