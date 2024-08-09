from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    @api.model
    def _teamm2odoo(self):
        TeamM = self.env ["teamm"]

        partner = self.env["res.partner"]._teamm2odoo_search()
        booking_type = TeamM.get_booking_type()
        start = TeamM._get_date("from")
        stop = TeamM._get_date("to")
        event_name = self.env["event.event"]._teamm2odoo_get_value("event.event")
        if event_name:
            # Identify a resource booking representing the event in timeline
            if not len(partner):
                partner = self.env.ref("base.main_partner")
            if not len(booking_type):
                booking_type = self.env.ref(
                    "event_sale_resource_booking_timeline.resource_booking_type_event"
                )
        else:
            # Assert "Private" or "Share room"
            privacy = self._teamm2odoo_get_value("room sharing")
            assert privacy in ("Private", "Share room")
        # Identify a resource_booking
        kwargs = {
            "partner_ids": partner.ids,
            "type_id": booking_type.id,
            "start": start,
            "duration": (stop - start).total_seconds() / 3600,
        }
        record = self._teamm2odoo_set_record(kwargs)
        return record

    @api.model
    def _teamm2odoo_values(self, kwargs={}):
        event_name = self._teamm2odoo_get_value("event.event")
        if event_name:
            kwargs |= {
                "name": event_name,
                "combination_auto_assign": 1,
            }
        else:
            partner = self.env["res.partner"]._teamm2odoo_search()
            product = self.env["product.product"]._teamm2odoo_search()
            combination = self.env["teamm"].get_booking_combination()
            kwargs |= {
                "name": partner.name,
                "combination_auto_assign": 0,
                "combination_id": combination.id,
                "product_id": product.id,
            }

        return super()._teamm2odoo_values(kwargs)
