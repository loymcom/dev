from odoo import _, api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        values = teamm_values
        domain = [("name", "=", values["Ordre nr. "])]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Order = self.env["sale.order"]
        OrderLine = self.env["sale.order.line"]
        Partner = self.env["res.partner"]
        TeamM = self.env["team.m"]

        values = teamm_values
        odoo_order_values = {
            "name": values['Ordre nr. '],
            "partner_id": Partner.search([('ref', "=", values['Record ID - Contact - Hubspot'])]).id,
            "date_order": TeamM._mdy_date(values['Booked at'])
        }
        return odoo_order_values
