from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _teamm2odoo_values(self, kwargs):
        # value_ids is formatted as odoo_values, not as kwargs
        odoo_values = super()._teamm2odoo_values(kwargs)
        Attribute = self.env["product.attribute"]

        attribute_line_ids = []

        attribute_names = Attribute._teamm2odoo_names()
        for name in attribute_names:
            Attribute = Attribute.with_context(**{"product.attribute": name})
            attribute = Attribute._teamm2odoo_search()
            attribute_line_ids.append(
                fields.Command.create(
                    {
                        "attribute_id": attribute.id,
                        "value_ids": [fields.Command.set(attribute.value_ids.ids)],
                    }
                )
            )
        odoo_values["attribute_line_ids"] = attribute_line_ids
        return odoo_values
