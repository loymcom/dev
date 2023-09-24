from odoo import api, fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    period_type = fields.Selection(
        [
            ("period", "Period"),
            ("statistics", "Include in Period Statistics"),
        ],
        string="Period Type"
    )
