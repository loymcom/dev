from odoo import api, fields, models

class Teamm(models.Model):
    _inherit = "teamm"

    def action_discounts_to_aliases(self):
        variants = self.env["teamm.discount.product.variant"].search([])
        for variant in variants:
            aliases = ", ".join(variant.discount_ids.mapped("name"))
            alias_record = self.alias_ids.filtered(lambda a: a.name == variant.name)
            if alias_record:
                alias_record.aliases = aliases
            else:
                alias_record = self.env["teamm.alias"].create(
                    {
                        "note": "discount",
                        "name": variant.name,
                        "aliases": aliases,
                        "teamm_id": self.id,
                    }
                )
