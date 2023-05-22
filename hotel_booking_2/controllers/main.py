import logging

from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class HotelBookingController(http.Controller):
    @http.route(['/hotel_booking/ui'], type='http', auth='public')
    def hotel_booking_ui(self, hotel_folio_id, **k):
        context = {"hotel_folio_id": hotel_folio_id}
        return request.render('hotel_booking_2.hotel_booking_index', context)
