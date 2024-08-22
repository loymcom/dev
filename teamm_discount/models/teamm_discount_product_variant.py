from odoo import api, fields, models

class TeammDiscountProductVariant(models.Model):
    _name = "teamm.discount.product.variant"
    _description = "teamm.discount.product.variant"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
    )
    discount_ids = fields.One2many(
        comodel_name="teamm.discount",
        inverse_name="variant_id",
    )
    product_id = fields.Many2one(
        comodel_name="teamm.discount.product",
    )
