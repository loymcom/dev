from odoo import api, fields, models

class FhRoomTypeOption(models.Model):
    _name = "fh.room.type.option"
    _description = "fh.room.type.option"

    name = fields.Char(
    )
    room_type_id = fields.Many2one(
        comodel_name="fh.room.type",
    )
    price = fields.Integer(
    )
