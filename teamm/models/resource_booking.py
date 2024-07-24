from datetime import datetime

from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)

""" This handles both regular bookings and booking periods. """

class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    @api.model
    def _teamm2odoo_search(self, teamm_values, combination=None):
        product, partner, start, stop = self._teamm2odoo_search_fields(teamm_values)
        if combination:
            domain = [
                ("combination_id", "=", combination.id),
                ("start", "=", start),
                ("stop", "=", stop),
            ]
        else:
            domain = [
                ("product_id", "=", product.id),
                ("partner_ids", "in", partner.ids),
                ("start", "=", start),
                ("stop", "=", stop),
            ]
        return self.search(domain)
    
    @api.model
    def _teamm2odoo_search_fields(self, teamm_values):
        TeamM = self.env ["teamm"]
        product = self.env["product.product"]._teamm2odoo_search(teamm_values)
        partner = self.env["res.partner"]._teamm2odoo_search(teamm_values)
        start = TeamM._get_date(teamm_values["from"])
        stop = TeamM._get_date(teamm_values["to"])
        return product, partner, start, stop

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        val = teamm_values
        product, partner, start, stop = self._teamm2odoo_search_fields(teamm_values)
        type = self.env["resource.booking.type"]._teamm2odoo_search(teamm_values)
        combinations = type.combination_rel_ids.combination_id.filtered(
            lambda c: val.get("room") or val.get("resource.resource") in c.display_name
        )
        session = teamm_values.get("session number")
        if session:
            session = self.search(
                [("name", "=", session), ("period_type", "=", "period")]
            )
        # There may be 2 possible combinations. Select the first which is available.
        for combination in combinations:
            booking = self._teamm2odoo_search(teamm_values, combination)
            if not booking or booking.partner_id == partner:
                order = self.env["sale.order"]._teamm2odoo_search(teamm_values)
                orderline = self.env["sale.order.line"]._teamm2odoo_search(teamm_values)
                odoo_values = {
                    "name": partner.name if session else teamm_values["name"],
                    "parent_id": session.id if session else False,
                    "sale_order_id": order.id if order else False,
                    "sale_order_line_id": orderline.id if orderline else False,
                    "product_id": product.id,
                    "partner_id": partner.id,
                    "start": start,
                    "duration": (stop - start).total_seconds() / 3600,
                    "type_id": type.id,
                    "combination_id": combination.id,
                    "combination_auto_assign": False,
                }
                return odoo_values

    @api.model
    def _teamm2odoo_after_create(self, record):
        record.sale_order_line_id.resource_booking_id = record.id
