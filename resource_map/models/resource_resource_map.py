from odoo import fields, models

class ResourceMap(models.Model):
    _name = "resource.resource.map"

    name = fields.Char()
    resource_ids = fields.One2many("resource.resource", "map_id", string="Resources")
