from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"


    hubspot_contact_id = fields.Char()
