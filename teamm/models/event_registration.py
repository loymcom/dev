from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model
    def _teamm2odoo(self):
        session_number = self._teamm2odoo_get_value("session number")
        event = self.env["event.event"]._teamm2odoo_search({"name": session_number})
        booking = self.env["resource.booking"]._teamm2odoo_search()
        kwargs = {
            "event_id": event.id,
            "resource_booking_id": booking.id,
        }
        records = self._teamm2odoo_set_record(kwargs)
        return records

    @api.model
    def _teamm2odoo_values(self, kwargs):
        first_name = self._teamm2odoo_get_value("first name")
        last_name = self._teamm2odoo_get_value("last name")
        name = "{} {}".format(first_name, last_name)
        kwargs |= {
            "name": name,
        }
        return super()._teamm2odoo_values(kwargs)

    def _teamm2odoo_after_create(self):
        booking = self.env["resource.booking"]._teamm2odoo_search()
        booking.event_registration_id = self.id
