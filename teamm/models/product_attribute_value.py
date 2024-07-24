from odoo import _, api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        attribute = self.env["product.attribute"]._teamm2odoo_search(teamm_values)
        domain = [
            ("name", "=", teamm_values["product.attribute.value"]),
            ("attribute_id", "=", attribute.id),
        ]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        attribute = self.env["product.attribute"]._teamm2odoo_search(teamm_values)
        booking_type = self.env["resource.booking.type"].search(
            [("name", "=", teamm_values["product.attribute.value"])]
        )
        odoo_values = {
            "name": teamm_values["product.attribute.value"],
            "attribute_id": attribute.id,
            "resource_booking_type_id": booking_type.id or False,
        }
        return odoo_values
