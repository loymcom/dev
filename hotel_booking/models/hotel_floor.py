from odoo import models, fields

class RoomType(models.Model):
    _inherit = "hotel.room.type"

    active = fields.Boolean(default=True)
    background_color = fields.Char('Background Color', help='The background color of the floor in a html-compatible format', default='rgb(210, 210, 210)')
    background_image = fields.Binary('Background Image')
    room_ids = fields.One2many('hotel.room', 'room_categ_id', string='Rooms')
    sequence = fields.Integer('Sequence', default=1)

    """
    restaurant.floor is similar to hotel.room.type
    floor_id -> room_categ_id
    seats -> capacity
    shape -> (nothing)
    """
