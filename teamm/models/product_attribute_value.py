from odoo import _, api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.model
    def _teamm2odoo(self):
        records = self
        names = self._teamm2odoo_names()
        for name in names:
            self = self.with_context(**{"product.attribute.value": name})
            records |= self._teamm2odoo_set_record()
        return records
    
    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        kwargs["attribute_id"] =self.env["product.attribute"]._teamm2odoo_search().id

        discount = self.env.context.get("teamm_discount")
        if discount:
            kwargs["name"] = discount.name
        else:
            kwargs["name"] = self._teamm2odoo_name()

        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        booking_type = self.env["resource.booking.type"]._teamm2odoo_search()
        # TODO: Add support for multiple booking types
        kwargs["resource_booking_type_ids"] = booking_type.ids
        return super()._teamm2odoo_values(kwargs)
