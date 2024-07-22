from odoo import _, api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _team_m_to_odoo_search(self, team_m_values):
        values = team_m_values
        # return [("name", "=", values["name"])]
        domain = []
        return self.search(domain)

    @api.model
    def _team_m_to_odoo_values(self, team_m_values):
        Order = self.env["sale.order"]
        OrderLine = self.env["sale.order.line"]
        Partner = self.env["res.partner"]
        TeamM = self.env["team.m"]

        values = team_m_values
        odoo_order_line_values = {
            "order_id": Order._team_m_to_odoo_search(values).id,
            "product_id": 1,
            'start_date': TeamM._mdy_date(values['From']),
            'end_date': TeamM._mdy_date(values['To']),
            "product_uom_qty": 1,
            "price_unit": 10000,
        }
        return odoo_order_line_values
