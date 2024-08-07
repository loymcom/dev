import json
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale_product_variant.controllers.main import WebsiteSaleProductVariant


class WebsiteSaleFilter(WebsiteSaleProductVariant):

    def _get_filters(self, filters=[]):
        # List of filters to show on the left side of /shop.
        # Display type: 'select' or 'radio'
        # [(plural_name, model_name, domain, priority, display_type)]
        # e.g. [("brands", "product.brand", [], 10, "radio")]
        filters.sort(key=lambda x: x[3]) # Sort by priority
        return filters

    @http.route()
    def shop(self, page=0, category=None, brand=None, ppg=False, search="", **post):
        res = super().shop(
            page=page, category=category, search=search, brand=brand, ppg=ppg, **post
        )
        # Include filters and url arguments to keep
        keep = res.qcontext["keep"].args
        filters = []
        
        for plural_name, model, domain, priority, display_type in self._get_filters([]):
            keep[plural_name] = request.httprequest.args.getlist(plural_name)
            records = request.env[model].search(domain or [])
            selected_ids = [int(i) for i in keep[plural_name] if i]
            filters.append([plural_name, records, selected_ids, display_type])

        keep = QueryURL('/shop', **keep)
        res.qcontext.update(
            {
                "keep": keep,
                "filters": filters,
            }
        )
        return res
