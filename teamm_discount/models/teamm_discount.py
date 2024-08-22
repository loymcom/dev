from odoo import api, fields, models

class TeammDiscount(models.Model):
    _name = "teamm.discount"
    _description = "teamm.discount"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
    )
    variant_id = fields.Many2one(
        comodel_name="teamm.discount.product.variant",
    )
    product_id = fields.Many2one(
        comodel_name="teamm.discount.product",
        related="variant_id.product_id",
    )
