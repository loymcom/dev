from odoo import api, fields, models
from odoo.exceptions import UserError


class HotelFloor(models.Model):
    _inherit = "hotel.floor"

    # gallery view
    customer_id = fields.Many2one('res.partner', string="Customer")
    image_url = fields.Char('Image', help="encodes the url of the image")

    # map view
    room_ids = fields.One2many('hotel.room', 'floor_id', string='Rooms')

    def action_reserve_room_view_folio(self, room_id, context):
        self.ensure_one()
        values = {
            "product_id": self.env["hotel.room"].browse(room_id).product_id.id,
            "folio_id": context["folio_id"],
        }
        hotel_folio_line = self.env["hotel.folio.line"].create(values)
        hotel_folio = hotel_folio_line.folio_id

        return {
            "name": hotel_folio.display_name,
            "type": "ir.actions.act_window",
            "views": [[False, "form"]],
            "res_model": "hotel.folio",
            "res_id": hotel_folio.id,
        }
