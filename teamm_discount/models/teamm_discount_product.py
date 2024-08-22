from odoo import api, fields, models

class TeammDiscountProduct(models.Model):
    _name = "teamm.discount.product"
    _description = "teamm.discount.product"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
    )
    variant_ids = fields.One2many(
        comodel_name="teamm.discount.product.variant",
        inverse_name="product_id",
    )
    discount_ids = fields.One2many(
        comodel_name="teamm.discount",
        related="variant_ids.discount_ids",
    )
