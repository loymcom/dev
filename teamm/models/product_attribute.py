from odoo import _, api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    # @api.model
    # def _teamm2odoo_search(self, teamm_values):
    #     return super()._teamm2odoo_search(teamm_values)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        odoo_values = {
            "name": teamm_values["product.attribute"],
            "create_variant": teamm_values["create_variant"],
        }
        return odoo_values
