from odoo.http import request

from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    shop_model = fields.Selection(
        selection_add=[("website.event.booking.combination", "Event Booking Variant")]
    )

    def _product2pav(self):
        """ From product model, get the relation to product attribute values"""        
        if self.shop_model == "website.event.booking.combination":
            return "product_template_attribute_value_ids.product_attribute_value_id"

        return super()._product2pav()


    def sale_product_domain(self):
        domain = super(Website, self).sale_product_domain()

        if self.shop_model == "website.event.booking.combination":
            def ids(string):
                return [int(num) for num in string.split(",")]

            # event.event
            events = request.httprequest.args.get("event.event")
            if events:
                domain = ["&"] + domain + [("event_id", "in", ids(events))]
            # resource.booking.type
            types = request.httprequest.args.get("resource.booking.type")
            if types:
                domain = ["&"] + domain + [("resource_booking_type_id", "in", ids(types))]
            # resource.booking.combination
            items = request.httprequest.args.get("resource.booking.combination")
            if items:
                domain = ["&"] + domain + [("combination_id", "in", ids(items))]
        
        return domain
