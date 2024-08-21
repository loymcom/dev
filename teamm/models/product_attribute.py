from odoo import _, api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        discount = self.env.context.get("teamm_discount")
        if discount:
            kwargs["name"] = self.env["teamm"].DISCOUNT[self.env.lang]
        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        create_variant = self._teamm2odoo_get_value("create variant") or "always"
        kwargs["create_variant"] = create_variant
        return super()._teamm2odoo_values(kwargs)
