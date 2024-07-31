from odoo import fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    tag_ids = fields.Many2many(
        comodel_name="product.attribute.value.tag",
        relation="product_attribute_value_tag_rel",
    )
