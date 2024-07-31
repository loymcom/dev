from odoo import api, fields, models

class FhRoom(models.Model):
    _name = "fh.room"
    _description = "fh.room"

    code = fields.Char(
    )
    name = fields.Char(
    )
    floor = fields.Integer(
    )
    view = fields.Char(
    )
    wing = fields.Char(
    )
    location_id = fields.Many2one(
        comodel_name="fh.location",
    )
    room_type_id = fields.Many2one(
        comodel_name="fh.room.type",
    )
    bed_space_ids = fields.One2many(
        comodel_name="fh.bed.space",
        inverse_name="room_id",
    )
