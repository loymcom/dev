from datetime import datetime

from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

def _parse_discounts(teamm_values):
    # Return {"discount1": amount1, "discount2": amount2}
    output = {}
    discounts = teamm_values["discounts"].split(", ")
    for discount in discounts:
        elements = discount.split(": ")
        key = ': '.join(elements[:-1])
        value = elements[-1]
        if value[-1] == "%":
            value = int(teamm_values["subtotal"]) * int(value[:-1]) / 100
        else:
            value = int(value)
        output[key] = value
    return output


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        order, product, partner, start_date, end_date = self._teamm2odoo_search_fields(
            teamm_values
        )
        domain = [
            ("order_id", "=", order.id),
            ("product_id", "=", product.id),
            ("partner_id", "=", partner.id),
            ("start_date", "=", start_date),
            ("end_date", "=", end_date),
        ]
        return self.search(domain)
    
    @api.model
    def _teamm2odoo_search_fields(self, teamm_values):
        order = self.env["sale.order"]._teamm2odoo_search(teamm_values)
        product = self.env["product.product"]._teamm2odoo_search(teamm_values)
        partner = self.env["res.partner"]._teamm2odoo_search(teamm_values)
        start_date = self.env["teamm"]._get_date(teamm_values["from"]).date()
        end_date = self.env["teamm"]._get_date(teamm_values["to"]).date()
        return order, product, partner, start_date, end_date

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        order, product, partner, start_date, end_date = self._teamm2odoo_search_fields(
            teamm_values
        )
        booking = self.env["resource.booking"]._teamm2odoo_search(teamm_values)
        _logger.warning(booking)
        odoo_values = {
            "order_id": order.id,
            "product_id": product.id,
            "name": product.display_name,
            "partner_id": partner.id,
            "start_date": start_date,
            "end_date": end_date,
            "product_uom_qty": 1,
            "price_unit": teamm_values["subtotal"],
            "resource_booking_id": booking.id,
        }
        discounts = _parse_discounts(teamm_values)
        if discounts:
            odoo_values = [odoo_values]
            for disc_name, disc_amount in discounts.items():
                Product = self.env["product.product"]
                disc_product = Product._teamm2odoo_search(teamm_values, disc_name)
                disc_values = odoo_values[0].copy()
                disc_values.update(
                    {
                        "product_id": disc_product.id,
                        "name": disc_product.display_name,
                        "price_unit": -disc_amount,
                    }
                )
                odoo_values.append(disc_values)
        return odoo_values

    @api.model
    def _teamm2odoo_after_create(self, records):
        record = records.filtered("product_id.resource_booking_type_id")
        record.resource_booking_id.sale_order_line_id = record.id
        record.resource_booking_id.sale_order_id = record.order_id.id
