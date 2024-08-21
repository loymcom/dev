import re

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


# def _parse_discounts(teamm_values):
#     output = []
#     discounts = teamm_values.get("discounts")
#     if discounts:
#         for discount in discounts.split(", "):
#             elements = discount.split(": ")
#             key = ': '.join(elements[:-1])
#             # FIXME: Do not hardcode "gavekort" here
#             if key.lower().startswith("gavekort"):
#                 key = "Gavekort"
#             value = elements[-1]
#             try:
#                 if value[-1] == "%":
#                     value = int(teamm_values["subtotal"]) * int(value[:-1]) / 100
#                 else:
#                     value = int(value)
#             except:
#                 hubspot_deal_id = teamm_values.get("hubspot deal id")
#                 raise ValidationError(f"Discount: {discount}\nDeal: {hubspot_deal_id}")
#             output.append(Discount(key, value))
#     return output

        
def _parse_discounts(self):
    teamm_aliases = self.env.context["teamm_aliases"]
    teamm_values = self.env.context["teamm_values"]

    # Input string
    input_string = teamm_values.get("discounts")

    # Dictionary for replacing certain discount names
    replacement_dict = {
        alias_name: name
        for name, aliases in teamm_aliases.items()
        for alias_name in aliases
    }

    # Function to replace discount names based on the dictionary
    def replace_discount_name(name):
        # Check if the name starts with "Gavekort" or "GAVEKORT"
        if name.startswith("Gavekort") or name.startswith("GAVEKORT"):
            return "Gavekort"
        # Check for replacements in the dictionary
        return replacement_dict.get(name.strip(), name.strip())

    def replace_discount_value(value):
        try:
            if value[-1] == "%":
                value = int(teamm_values["subtotal"]) * int(value[:-1]) / 100
            else:
                value = int(value)
            return value
        except:
            hubspot_deal_id = teamm_values.get("hubspot deal id")
            raise ValidationError(f"Discount error on deal {hubspot_deal_id}")

    # Find all discounts in the string
    discounts = re.findall(r'(?<!\w), ([^:]+): (\d+)', input_string)
    if discounts:
        # Convert the found discounts into a list of tuples with replacements
        discount_list = [
            (replace_discount_name(name), replace_discount_value(value))
            for name, value in discounts
            if name != "Total discount"
        ]

        # Calculate the total discount and the unknown discount
        total_discount = int(re.search(r'Total discount: (\d+)', input_string).group(1))
        known_discount = sum(value for _, value in discount_list)
        unknown_discount = total_discount - known_discount

        # Add the unknown discount to the list
        discount_list.append((self.env["teamm"].UNKNOWN_DISCOUNT[self.env.lang], unknown_discount))
        return discount_list
    else:
        return []


# class Discount(object):
#     def __init__(self, name, amount):
#         self.name = name
#         self.amount = amount


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _teamm2odoo(self):
        records = self._teamm2odoo_set_record()

        # FIXME: Temporarily disabled discounts
        discounts = _parse_discounts(self)
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
