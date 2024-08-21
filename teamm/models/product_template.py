from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _teamm2odoo_values(self, kwargs):
        return super()._teamm2odoo_values(kwargs)
