from odoo import api, fields, models

class ResourceCategory(models.Model):
    _name = "resource.category"
    _description = "resource.category"

    name = fields.Char()
