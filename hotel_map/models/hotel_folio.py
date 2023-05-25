from odoo import api, fields, models


class HotelFolio(models.Model):
    _inherit = "hotel.folio"

    def action_view_hotel_floor_map(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "res_model": "hotel.floor",
            "views": [[self.env.ref("hotel_map.hotel_floor_view_map_action_folio_add_room").id, "map"]],
            "context": {"folio_id": self.id},  # folio.room.line field
        }
        return action
