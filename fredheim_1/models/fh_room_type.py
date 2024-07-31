from odoo import api, fields, models

class FhRoomType(models.Model):
    _name = "fh.room.type"
    _description = "fh.room.type"

    name = fields.Char(
    )
    price = fields.Integer(
    )
    no_of_beds = fields.Integer(
    )
    has_sink = fields.Boolean(
    )
    has_toilet = fields.Boolean(
    )
    has_shower = fields.Boolean(
    )
    has_bathtub = fields.Boolean(
    )
    option_ids = fields.One2many(
        comodel_name="fh.room.type.option",
        inverse_name="room_type_id",
    )
