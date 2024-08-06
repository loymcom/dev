import json

from odoo import http
from odoo.http import request, Controller
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_sale_product_variant.controllers.main import WebsiteSaleProductVariant

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


class WebsiteSaleBooking(WebsiteSaleProductVariant):

    def _tmpl_ids(self, search_product, website):
        if website.shop_model == "website.event.booking.combination":
            return search_product.product_tmpl_id.ids

        return super()._tmpl_ids(search_product, website)


    # def _shop_get_query_url_kwargs(self, category, search, min_price, max_price, attrib=None, order=None, **post):
    #     result = super()._shop_get_query_url_kwargs(category, search, min_price, max_price, attrib=None, order=None, **post)
    #     # if post.get("events"):
    #     #     result["events"] = post["events"]
    #     return result
