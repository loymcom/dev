from datetime import datetime

from odoo import api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.model
    def search(self, domain, offset=0, limit=None, order=None, count=False):
        records = super().search(domain, offset, limit, order, count)

        if self.env.context.get("shop_model") == "website.event.booking.combination":

            # Create dummy records for filtering in /shop
            now = datetime.now()
            for ee in self.env["event.event"].search([("date_end", ">", now)]):
                records |= self.new({"name": ee.name, "attribute_id": "ee"}, ref="ee" + str(ee.id))
                # records |= self.new({"id": "ee" + str(ee.id), "name": ee.name, "attribute_id": "ee"})

            for rbc in self.env["resource.booking.combination"].search([]):
                records |= self.new({"name": rbc.name, "attribute_id": "rbc"}, ref="rbc" + str(rbc.id))

        return records
