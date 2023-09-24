from odoo import api, fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    period_statistics = fields.Boolean("Period Statistics")
