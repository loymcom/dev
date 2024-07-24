from datetime import datetime

from odoo import _, api, fields, models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        bookingtype = self.env["resource.booking.type"]._teamm2odoo_search(teamm_values)
        # if bookingtype.period_type == "period":
        #     pass
        # else:
        product, partner, start, stop = self._teamm2odoo_search_fields(teamm_values)
        domain = [
            ("product_id", "=", product.id),
            ("partner_id", "=", partner.id),
            ("start", "=", start),
            ("stop", "=", stop),
        ]
        return self.search(domain)
    
    @api.model
    def _teamm2odoo_search_fields(self, teamm_values):
        TeamM = self.env ["teamm"]
        product = self.env["product.product"]._teamm2odoo_search(teamm_values)
        partner = self.env["res.partner"]._teamm2odoo_search(teamm_values)
        # start = datetime.strptime(teamm_values["from"], "%b %d, %Y")
        # stop = datetime.strptime(teamm_values["to"], "%b %d, %Y")
        start = TeamM._get_date(teamm_values["from"])
        stop = TeamM._get_date(teamm_values["to"])
        return product, partner, start, stop

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        product, partner, start, stop = self._teamm2odoo_search_fields(teamm_values)
        type = self.env["resource.booking.type"]._teamm2odoo_search(teamm_values)
        comb = self.env["resource.booking.combination"]._teamm2odoo_search(teamm_values)
        
        odoo_values = {
            "product_id": product.id,
            "partner_id": partner.id,
            "start": start,
            "stop": stop,
            "type_id": type.id,
            "combination_id": comb.id,
            "combination_auto_assign": False,
        }
        return odoo_values
