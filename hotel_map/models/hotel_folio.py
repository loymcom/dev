from odoo import api, fields, models


class HotelFolio(models.Model):
    _inherit = "hotel.folio"

    def action_view_floor_map_select_room(self):
        self.ensure_one()
        return {
            "name": "Select Room",
            "type": "ir.actions.act_window",
            "res_model": "hotel.floor",
            "views": [
                [self.env.ref("hotel_map.hotel_floor_view_map_select_room").id, "map"]
            ],
            "context": {"folio_id": self.id},
        }
