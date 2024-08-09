from odoo import _, api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.model
    def _teamm2odoo(self):
        Attribute = self.env["product.attribute"]
        names = self._teamm2odoo_names()
        for name in names:
            attribute = Attribute._teamm2odoo_search()
            record = self._teamm2odoo_set_record(
                {"name": name, "attribute_id": attribute.id}
            )
        return record

    @api.model
    def _teamm2odoo_values(self, kwargs):
        booking_type = self.env["resource.booking.type"]._teamm2odoo_search()
        # TODO: Add support for multiple booking types
        kwargs["resource_booking_type_ids"] = booking_type.ids
        return super()._teamm2odoo_values(kwargs)
