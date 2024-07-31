from odoo import fields, models


class ProductAttributeValueTag(models.Model):
    _name = "product.attribute.value.tag"

    name = fields.Char()
    # pav_ids = fields.Many2many(
    #     comodel_name="product.attribute.value",
    #     relation="product_attribute_value_tag_rel",
    # )
