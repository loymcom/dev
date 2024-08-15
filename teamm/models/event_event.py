from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class EventEvent(models.Model):
    _inherit = "event.event"
    
    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        TeamM = self.env ["teamm"]
        kwargs |= {"name": self._teamm2odoo_name()}

        create_event = bool(self.env.context["teamm"].model_ids.filtered(lambda m: m.name == "event.event"))
        if create_event:
            kwargs |= {
                "date_begin": TeamM._get_datetime("from"),
                "date_end": TeamM._get_datetime("to"),
            }

        return kwargs

    @api.model
    def _teamm2odoo_values(self, kwargs):
        # Multiple products names, therefore .search() instead of ._teamm2odoo_search()
        product_names = self.env["product.template"]._teamm2odoo_names()
        products = self.env["product.template"].search([("name", "in", product_names)])
        kwargs |= {
            "resource_booking_id": self.env["resource.booking"]._teamm2odoo_search().id,
            "product_tmpl_ids": products.ids,
        }
        odoo_values = super()._teamm2odoo_values(kwargs)

        # # FIXME: EVENT PRODUCT variable
        # odoo_values |= {
        #     "event_ticket_ids": [
        #         fields.Command.create(
        #             {
        #                 "product_id": self.env["product.product"].search(
        #                     [("name", "=", "EVENT PRODUCT")]
        #                 ).id,
        #             }
        #         )
        #     ],
        # }
        return odoo_values
