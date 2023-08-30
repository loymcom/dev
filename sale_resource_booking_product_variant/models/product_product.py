from datetime import datetime

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _default_resource_booking_type_id(self):
        return self.product_tmpl_id.resource_booking_type_id

    def _default_resource_booking_type_combination_rel_id(self):
        return self.product_tmpl_id.resource_booking_type_combination_rel_id

    resource_booking_type_id = fields.Many2one(
        "resource.booking.type",
        string="Booking type",
        index=True,
        ondelete="restrict",
        help="If set, one pending booking will be generated when sold.",
        default=lambda self: self._default_resource_booking_type_id(),
    )
    resource_booking_type_combination_rel_id = fields.Many2one(
        "resource.booking.type.combination.rel",
        string="Resource combination",
        index=True,
        ondelete="restrict",
        domain="[('type_id', '=', resource_booking_type_id)]",
        help=(
            "If set, the booking will be created with this resource combination. "
            "Otherwise, the combination will be assigned automatically later, "
            "when the requester schedules the booking."
        ),
        default=lambda self: self._default_resource_booking_type_combination_rel_id(),
    )

    def create(self, vals_list):
        products = super().create(vals_list)

        # Get values from product.attribute.value
        for product in products:
            type = set(ptav.product_attribute_value_id.resource_booking_type_id for ptav in product.product_template_attribute_value_ids)
            if type and len(type) == 1:
                product.resource_booking_type_id = type.pop().id
            type_combination_rel = set(ptav.product_attribute_value_id.resource_booking_type_combination_rel_id for ptav in product.product_template_attribute_value_ids)
            if type_combination_rel and len(type_combination_rel) == 1:
                product.resource_booking_type_combination_rel_id = type_combination_rel.pop().id

        return products

    def action_view_resource_booking(self):
        action = super().action_view_resource_booking()
        action["context"]["default_partner_id"] = self.partner_id.id
        return action
