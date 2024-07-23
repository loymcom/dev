from odoo import _, api, fields, models

class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        domain = [("name", "=", teamm_values["attribute"])]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        odoo_values = {"name": teamm_values["attribute"]}
        return odoo_values
