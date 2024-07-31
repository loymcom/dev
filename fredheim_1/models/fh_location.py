from odoo import api, fields, models

class FhLocation(models.Model):
    _name = "fh.location"
    _description = "fh.location"

    name = fields.Char(
        relation="id",
    )
