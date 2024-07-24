from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # @api.model
    # def _teamm2odoo_search(self, teamm_values):
    #     return super()._teamm2odoo_search(teamm_values)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Partner = self.env["res.partner"]
        TeamM = self.env["teamm"]
        val = teamm_values
        if val["main guest"] == "Yes":
            odoo_values = {
                "name": val["sale.order"],
                "partner_id": Partner.search([("ref", "=", val["hubspot contact"])]).id,
                "date_order": TeamM._get_date(val["booked at"])
            }
            return odoo_values
