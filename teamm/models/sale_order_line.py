from odoo import _, api, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _teamm2odoo(self):
        records = self._teamm2odoo_set_record()

        discounts = self._teamm2odoo_get_value("discounts")
        for discount in discounts:
            self = self.with_context(teamm_discount=discount)
            records |= self._teamm2odoo_set_record()

        return records

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        order = self.env["sale.order"]._teamm2odoo_search()
        booking = self.env["resource.booking"]._teamm2odoo_search()
        product = self.env["product.product"]._teamm2odoo_search()
        if not len(order) or not len(booking) or not len(product):
            raise ValidationError(f"Missing info:\nOrder: {order}\nProduct: {product}\nBooking: {booking}")
        kwargs |= {
            "order_id": order.id,
            "resource_booking_id": booking.id,
            "product_id": product.id,
        }
        return super()._teamm2odoo_search_kwargs(kwargs)
    
    @api.model
    def _teamm2odoo_values(self, kwargs):
        TeamM = self.env ["teamm"]

        # values
        product = self.env["product.product"]._teamm2odoo_search()
        start_date = TeamM._get_date("from")
        end_date = TeamM._get_date("to")
        if not len(product):
            debug = True
        kwargs |= {
            "name": product.display_name,
            "product_uom_qty": 1,
            "start_date": start_date,
            "end_date": end_date,
            "currency_id": self.env.company.currency_id.id,
        }

        # conditional values
        discount = self.env.context.get("teamm_discount")
        if discount:
            price_unit = -discount[1]
        else:
            price_unit = self._teamm2odoo_get_value("subtotal")
        kwargs ["price_unit"] = price_unit
        
        return super()._teamm2odoo_values(kwargs)

    @api.model
    def _teamm2odoo_after_create(self):
        record = self.filtered("product_id.resource_booking_type_id")
        record.resource_booking_id.sale_order_line_id = record.id
        record.resource_booking_id.sale_order_id = record.order_id.id
