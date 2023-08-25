from odoo import fields, models

class ResourceBookingSale(models.TransientModel):
    _inherit = "resource.booking.sale"

    date_range_id = fields.Many2one("date.range", string="Date Range")
