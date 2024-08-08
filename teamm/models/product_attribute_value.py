from odoo import _, api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.model
    def _teamm2odoo(self):
        TeamM = self.env["teamm"]
        names = self._teamm2odoo_names()
        for name in names:
            record = self._teamm2odoo_search({"name": name})
            odoo_values = self._teamm2odoo_values(name)
            record = record._teamm2odoo_set_record(odoo_values)
        return record
    
    @api.model
    def _teamm2odoo_domain(self, kwargs):
        domain = super()._teamm2odoo_domain(kwargs)
        attribute = self.env["product.attribute"]._teamm2odoo_search({})
        domain += [("attribute_id", "=", attribute.id)]
        return domain
    
    @api.model
    def _teamm2odoo_values(self, name):
        attribute = self.env["product.attribute"]._teamm2odoo_search({})
        booking_type = self.env["resource.booking.type"]._teamm2odoo_search({})
        odoo_values = {
            "name": name,
            "attribute_id": attribute.id,
            "resource_booking_type_id": booking_type.id,
        }
        return odoo_values
