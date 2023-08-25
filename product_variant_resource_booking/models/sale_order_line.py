from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    start = fields.Many2one("product.attribute.value", string="Product Attribute Value")
