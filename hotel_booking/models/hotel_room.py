from odoo import models, fields

class HotelRoom(models.Model):
    _inherit = "hotel.room"

    position_h = fields.Float('Horizontal Position', default=10,
        help="The table's horizontal position from the left side to the table's center, in pixels")
    position_v = fields.Float('Vertical Position', default=10,
        help="The table's vertical position from the top to the table's center, in pixels")
    width = fields.Float('Width', default=50, help="The table's width in pixels")
    height = fields.Float('Height', default=50, help="The table's height in pixels")
    color = fields.Char('Color', help="The table's color, expressed as a valid 'background' CSS property value")

    """
    restaurant.table is similar to hotel.room
    table_ids -> room_ids
    pos_config_id -> (nothing)
    """
