from odoo import _, api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        values = teamm_values
        # return [("name", "=", values["name"])]
        domain = []
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Order = self.env["sale.order"]
        OrderLine = self.env["sale.order.line"]
        Partner = self.env["res.partner"]
        TeamM = self.env["teamm"]

        values = teamm_values
        odoo_order_line_values = {
            "order_id": Order._teamm2odoo_search(values).id,
            "product_id": 1,
            'start_date': TeamM._mdy_date(values['From']),
            'end_date': TeamM._mdy_date(values['To']),
            "product_uom_qty": 1,
            "price_unit": 10000,
        }
        return odoo_order_line_values
