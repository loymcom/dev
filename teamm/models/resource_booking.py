from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

""" This handles both regular BOOKINGS and booking PERIODS. """
def _is_period(teamm_values):
    if teamm_values.get("resource.booking.type"):
        return True
    else:
        return False


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    @api.model
    def _teamm2odoo_search(self, teamm_values, combination=None):
        combinations, partner, product, session, start, stop, type = self._teamm2odoo_search_fields(teamm_values)
        # self.env["resource.booking.combination"]_teamm2odoo_sarch(teamm_values)
        if combination:
            # The combination comes from _teamm2odoo_values, see below
            domain = [
                ("combination_id", "=", combination.id),
                ("start", "=", start),
                ("stop", "=", stop),
            ]
        else:
            domain = [
                ("combination_id", "in", combinations.ids),
                ("partner_ids", "in", partner.ids),
                ("product_id", "=", product.id),
                ("start", "=", start),
                ("stop", "=", stop),
                ("type_id", "=", type.id),
            ]
        _logger.warning(domain)
        return self.search(domain)
    
    @api.model
    def _teamm2odoo_search_fields(self, teamm_values, period=False):
        TeamM = self.env ["teamm"]
        partner = self.env["res.partner"]._teamm2odoo_search(teamm_values)
        product = self.env["product.product"]._teamm2odoo_search(teamm_values)
        start = TeamM._get_date(teamm_values["from"])
        stop = TeamM._get_date(teamm_values["to"])
        type = self.env["resource.booking.type"]._teamm2odoo_search(teamm_values)
        if _is_period(teamm_values):
            combinations = type.combination_rel_ids.combination_id
            session = False
        else:
            combinations = type.combination_rel_ids.combination_id.filtered(
                lambda c: teamm_values.get("room") in c.display_name
            )
            session = teamm_values.get("session")
            if session:
                session = self.search(
                    [("name", "=", session), ("period_type", "=", "period")]
                )
        if not combinations:
            _logger.warning(partner.name)
            raise UserError("No combination")
        return combinations, partner, product, session, start, stop, type

    @api.model
    def _teamm2odoo_values(self, teamm_values, period=False):
        val = teamm_values
        combinations, partner, product, session, start, stop, type = self._teamm2odoo_search_fields(teamm_values)

        # There may be 2 possible combinations. Select the first which is available.
        for combination in combinations:
            booking = self._teamm2odoo_search(teamm_values, combination)
            if not booking or booking.partner_id == partner:
                _logger.warning(teamm_values["sale.order"] + " from " + teamm_values["from"] + " session " + str(session))
                odoo_values = {
                    "name": teamm_values.get("name") if _is_period(teamm_values) else partner.name,
                    "parent_id": session.id if session else False,
                    "product_id": product.id,
                    "partner_id": partner.id,
                    "start": start,
                    "duration": (stop - start).total_seconds() / 3600,
                    "type_id": type.id,
                    "combination_id": combination.id,
                    "combination_auto_assign": False,
                }
                return odoo_values
