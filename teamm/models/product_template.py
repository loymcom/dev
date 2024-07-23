from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        values = teamm_values
        domain = [("name", "=", values["program"].split()[0])]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        attribute_line_ids = []
        attributes = self.env["product.attribute"]._teamm2odoo_search(teamm_values)
        for attribute in attributes:
            attribute_line_ids.append(
                fields.Command.create(
                    {
                        "attribute_id": attribute.id,
                        "value_ids": [fields.Command.set(attribute.value_ids.ids)],
                    }
                )
            )
        odoo_values = {
            "name": teamm_values["program"],
            "attribute_line_ids": attribute_line_ids,
        }
        return odoo_values
