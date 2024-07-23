from odoo import _, api, fields, models

class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        domain = [("name", "in", teamm_values["attributes"].split(","))]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        odoo_values = [
            {"name": attribute} for attribute in teamm_values["attributes"].split(",")
        ]
        return odoo_values
