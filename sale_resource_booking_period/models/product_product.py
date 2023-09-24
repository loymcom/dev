from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_view_resource_booking(self):
        action = super().action_view_resource_booking()
        # Timeline view: Show periods and bookings with the product's combinations.
        combination_ids = self._get_resource_booking_combination_ids()
        action["domain"] = [
            "|",
            ("period_product_tmpl_ids", "in", self.product_tmpl_id.id),
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
