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
        combinations = request.env["event.booking.combination"].search(
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
        if website.shop_model == "event.booking.combination":
            return search_product.product_tmpl_id.ids

        return super()._tmpl_ids(search_product, website)


# class WebsiteEvent(WebsiteEventController):

#     def _process_attendees_form(self, event, form_details):
#         """ Process data posted from the attendee details form. """
#         registrations = super(WebsiteEvent, self)._process_attendees_form(event, form_details)

#         # for registration in registrations:
#         #     registration['registration_answer_ids'] = []

#         # general_answer_ids = []
#         # for key, value in form_details.items():
#         #     if 'question_answer' in key and value:
#         #         dummy, registration_index, question_id = key.split('-')
#         #         question_sudo = request.env['event.question'].browse(int(question_id))
#         #         answer_values = None
#         #         if question_sudo.question_type == 'simple_choice':
#         #             answer_values = {
#         #                 'question_id': int(question_id),
#         #                 'value_answer_id': int(value)
#         #             }
#         #         elif question_sudo.question_type == 'text_box':
#         #             answer_values = {
#         #                 'question_id': int(question_id),
#         #                 'value_text_box': value
#         #             }

#         #         if answer_values and not int(registration_index):
#         #             general_answer_ids.append((0, 0, answer_values))
#         #         elif answer_values:
#         #             registrations[int(registration_index) - 1]['registration_answer_ids'].append((0, 0, answer_values))

#         # for registration in registrations:
#         #     registration['registration_answer_ids'].extend(general_answer_ids)

#         return registrations
