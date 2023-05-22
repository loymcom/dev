import logging

from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class HotelFloorController(http.Controller):
    @http.route(['/hotel_floor/ui'], type='http', auth='public')
    def hotel_floor_ui(self, hotel_folio_id, **k):
        context = {"hotel_folio_id": hotel_folio_id}
        return request.render('hotel_booking_2.floor_index', context)
