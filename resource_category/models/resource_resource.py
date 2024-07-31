from odoo import api, fields, models

class ResourceResource(models.Model):
    _inherit = "resource.resource"

    category_id = fields.Many2one(
        comodel_name="resource.category",
        string="Category",
    )
    category_ids = fields.Many2many(
        comodel_name="resource.category",
        relation="resource_resource_category_rel",
        string="Categories",
    )
