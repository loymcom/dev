from datetime import datetime

from odoo import _, api, fields, models


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
        # start_date = datetime.strptime(teamm_values["from"], "%m/%d/%Y").date()
        # end_date = datetime.strptime(teamm_values["to"], "%m/%d/%Y").date()
        start_date = self.env["teamm"]._get_date(teamm_values["from"]).date()
        end_date = self.env["teamm"]._get_date(teamm_values["to"]).date()
        return order, product, partner, start_date, end_date

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        order, product, partner, start_date, end_date = self._teamm2odoo_search_fields(
            teamm_values
        )
        odoo_values = {
            "order_id": order.id,
            "product_id": product.id,
            "name": product.display_name,
            "partner_id": partner.id,
            "start_date": start_date,
            "end_date": end_date,
            "product_uom_qty": 1,
            "price_unit": teamm_values["subtotal"],
        }
        return odoo_values
