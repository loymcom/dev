from odoo import api, fields, models
from odoo.exceptions import UserError


class HotelFloor(models.Model):
    _inherit = "hotel.floor"

    # gallery view
    customer_id = fields.Many2one('res.partner', string="Customer")
    image_url = fields.Char('Image', help="encodes the url of the image")

    # map view
    room_ids = fields.One2many('hotel.room', 'floor_id', string='Rooms')
