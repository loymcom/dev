from odoo import api, fields, models

class DateRange(models.Model):
    _inherit = "date.range"

    product_template_ids = fields.Many2many(
        comodel_name="product.template",
        relation="product_template_date_range_rel",
        string="Products",
    )
