from odoo.addons.website_sale_product_variant.controllers.main import WebsiteSaleProductVariant


class WebsiteSaleBooking(WebsiteSaleProductVariant):

    def _tmpl_ids(self, search_product, website):
        if website.shop_model == "website.event.sale.resource.booking":
            return search_product.product_tmpl_id.ids

        return super()._tmpl_ids(search_product, website)
