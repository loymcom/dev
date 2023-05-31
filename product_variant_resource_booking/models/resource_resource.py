from odoo import api, fields, models

class ResourceResource(models.Model):
    _inherit = "resource.resource"

    product_attribute_value_id = fields.Many2one("product.attribute.value", string="Product Attribute Value")
