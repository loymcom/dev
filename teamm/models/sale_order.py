from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # @api.model
    # def _teamm2odoo_search(self, teamm_values):
    #     return super()._teamm2odoo_search(teamm_values)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Order = self.env["sale.order"]
        OrderLine = self.env["sale.order.line"]
        Partner = self.env["res.partner"]
        TeamM = self.env["teamm"]

        values = teamm_values
        odoo_values = {
            "name": values["sale.order"],
            "partner_id": Partner.search([("ref", "=", values["hubspot contact"])]).id,
            "date_order": TeamM._get_date(values["booked at"])
        }
        return odoo_values
