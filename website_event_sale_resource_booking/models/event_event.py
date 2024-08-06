from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    def get_available_products(self):
        self.ensure_one()
        records = self.env["event.booking.combination"].search(
            [
                ("event_id", "=", self.id),
                ("available", "=", True),
            ]
        )
        products = {record.product_id for record in records}
        return products

    # def get_available_combinations(self):
    #     self.ensure_one()
    #     records = self.env["event.booking.combination"].search(
    #         [
    #             ("event_id", "=", self.id),
    #             ("available", "=", True),
    #         ]
    #     )
    #     combinations = {record.combination_id for record in records}
    #     return combinations
