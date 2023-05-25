from odoo import api, fields, models


class HotelRoom(models.Model):
    _name = "hotel.room"
    _inherit = ['hotel.room', 'map.item.mixin']
