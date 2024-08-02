from odoo import api, fields, models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    session_id = fields.Many2one("resource.booking.session")
