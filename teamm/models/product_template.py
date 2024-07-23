from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        values = teamm_values
        domain = [("name", "=", values["Program"].split()[0])]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Order = self.env["sale.order"]
        OrderLine = self.env["sale.order.line"]
        Partner = self.env["res.partner"]
        TeamM = self.env["teamm"]

        values = teamm_values
        odoo_order_values = {
            "name": values['Ordre nr. '],
            "partner_id": Partner.search([('ref', "=", values['Record ID - Contact - Hubspot'])]).id,
            "date_order": TeamM._mdy_date(values['Booked at'])
        }
        return odoo_order_values
