from odoo import api, fields, models

class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    hubspot_deal_id = fields.Char()
