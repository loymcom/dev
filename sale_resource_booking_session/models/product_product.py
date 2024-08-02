from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_view_resource_booking(self):
        action = super().action_view_resource_booking()
        # Bookings to show:
        # 1. Bookings of this product
        # Timeline view must also show these bookings:
        # 2. Sessions related to this product
        # 3. Combinations related to this product
        combination_ids = self._get_resource_booking_combination_ids()
        action["domain"] = [
            "|",
            "|",
            ("product_id", "=", self.id),
            ("session_product_tmpl_ids", "in", self.product_tmpl_id.id),
            ("combination_id", "in", combination_ids),
        ]
        return action

    def _get_resource_booking_combination_ids(self):
        self.ensure_one()
        return (
            self.resource_booking_type_combination_rel_id.combination_id.id
            or
            self.resource_booking_type_id.combination_rel_ids.mapped(
                "combination_id"
            ).ids
        )
