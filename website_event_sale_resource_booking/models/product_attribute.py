from datetime import datetime

from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    @api.model
    def search(self, domain, offset=0, limit=None, order=None, count=False):
        records = super().search(domain, offset, limit, order, count)

        if self.env.context.get("shop_model") == "website.event.booking.combination":
            # Create dummy records for filtering in /shop
            records |= self.new({"name": "Event", "visibility": "visible"}, ref="ee")
            records |= self.new({"name":"Book", "visibility": "visible"}, ref="rbc")
            # records |= self.new({"id": "ee", "name": "Event", "visibility": "visible"})
            # records |= self.new({"id": "rbc", "name":"Book", "visibility": "visible"})
        return records
