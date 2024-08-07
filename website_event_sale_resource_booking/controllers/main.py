import json

from datetime import datetime

from odoo import http
from odoo.http import request

from odoo.addons.website_sale_filter.controllers.main import WebsiteSaleFilter

import logging
_logger = logging.getLogger(__name__)

    
class EventRegistration(http.Controller):

    @http.route('/event/get_available_combinations', type='http', auth='public')
    def get_combinations(self, event_id, product_id):
        combinations = request.env["website.event.booking.combination"].search(
            [
                ("event_id", "=", int(event_id)),
                ('product_id', '=', int(product_id)),
                ("available", "=", True),
            ]
        )
        _logger.info("Fetched combinations: %s", combinations)
        combi_list = [
            {'id': comb.combination_id.id, 'name': comb.combination_id.name}
            for comb in combinations
        ]
        return json.dumps(combi_list)


class WebsiteSaleBooking(WebsiteSaleFilter):

    def _tmpl_ids(self, search_product, website):
        if website.shop_model == "website.event.booking.combination":
            return search_product.product_tmpl_id.ids

        return super()._tmpl_ids(search_product, website)
    

    def _get_filters(self, filters=[]):
        # List of (plural_name, model_name, domain, priority)
        filters.append(
            ["events", "event.event", [("date_end", ">", datetime.now())], 5, "select"]
        )
        filters.append(["types", "resource.booking.type", [], 40, "select"])
        filters.append(["items", "resource.booking.combination", [], 50, "select"])
        return super()._get_filters(filters)
