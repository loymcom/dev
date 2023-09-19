from odoo import fields, models

class Resource(models.Model):
    _name = "resource.resource"
    _inherit = ["resource.resource", "map.item.mixin"]

    map_id = fields.Many2one("resource.resource.map")
