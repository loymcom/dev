from odoo import api, fields, models

class FhBedSpace(models.Model):
    _name = "fh.bed.space"
    _description = "fh.bed.space"

    name = fields.Char(
    )
    type = fields.Selection(
        selection=[('1', 'Single Bed'), ('2', 'Double Bed'), ('3', 'Triple Bed')],
    )
    room_id = fields.Many2one(
        comodel_name="fh.room",
    )
