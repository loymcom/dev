import logging

from odoo import http, _
from odoo.http import request
from odoo.addons.account.controllers.portal import PortalAccount

_logger = logging.getLogger(__name__)


class PosController(PortalAccount):

    @http.route(['/floor/ui'], type='http', auth='public')
    def floor_ui(self, hotel_floor_id=False, **k):
        context = {}
        response = request.render('hotel_booking_2.floor_index', context)
        response.headers['Cache-Control'] = 'no-store'
        return response


class OwlPlayground(http.Controller):
    @http.route(['/owl_playground/playground'], type='http', auth='public')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render('hotel_booking_2.floor_index_2')
