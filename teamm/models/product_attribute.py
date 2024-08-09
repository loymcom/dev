from odoo import _, api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    @api.model
    def _teamm2odoo_values(self, kwargs):
        odoo_values = super()._teamm2odoo_values(kwargs)
        create_variant = self._teamm2odoo_get_value("create variant") or "always"
        odoo_values["create_variant"] = create_variant
        return odoo_values
