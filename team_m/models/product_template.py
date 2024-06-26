from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _team_m_search(self, team_m_values):
        """ Return search domain """
        values = team_m_values
        return [("name", "=", values["Program"].split()[0])]

    @api.model
    def _team_m_to_odoo(self, team_m_values):
        """ Return odoo values """

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
