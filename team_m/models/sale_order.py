from odoo import _, api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _team_m_to_odoo_search(self, team_m_values):
        values = team_m_values
        domain = [("name", "=", values["Ordre nr. "])]
        return self.search(domain)

    @api.model
    def _team_m_to_odoo_values(self, team_m_values):
        Order = self.env["sale.order"]
        OrderLine = self.env["sale.order.line"]
        Partner = self.env["res.partner"]
        TeamM = self.env["team.m"]

        values = team_m_values
        odoo_order_values = {
            "name": values['Ordre nr. '],
            "partner_id": Partner.search([('ref', "=", values['Record ID - Contact - Hubspot'])]).id,
            "date_order": TeamM._mdy_date(values['Booked at'])
        }
        return odoo_order_values
