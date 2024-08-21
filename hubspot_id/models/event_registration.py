from odoo import api, fields, models

class EventRegistration(models.Model):
    _inherit = "event.registration"

    hubspot_deal_id = fields.Char()
