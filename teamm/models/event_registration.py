from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        hubspot_deal_id = self._teamm2odoo_get_value("hubspot deal id")
        kwargs |= {
            "hubspot_deal_id": hubspot_deal_id,
        }
        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        event = self.env["event.event"]._teamm2odoo_search()
        booking = self.env["resource.booking"]._teamm2odoo_search()
        kwargs |= {
            "name": booking.partner_id.name,
            "email": booking.partner_id.email,
            "phone": booking.partner_id.mobile,
            "event_id": event.id,
            "resource_booking_id": booking.id,
        }
        return super()._teamm2odoo_values(kwargs)

    def _teamm2odoo_after_create(self):
        booking = self.env["resource.booking"]._teamm2odoo_search()
        booking.event_registration_id = self.id
