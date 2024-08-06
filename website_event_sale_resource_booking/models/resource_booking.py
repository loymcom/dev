from odoo import fields,models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    # resource_id = fields.Many2many(
    #     "resource.resource",
    #     related="combination_id.resource_id",
    # )
