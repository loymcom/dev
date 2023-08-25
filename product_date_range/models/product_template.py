from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    date_range_ids = fields.Many2many(
        comodel_name="date.range",
        relation="product_template_date_range_rel",
        string="Date Ranges",
    )
