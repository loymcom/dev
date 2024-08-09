from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class EventEvent(models.Model):
    _inherit = "event.event"

    @api.model
    def _teamm2odoo(self):
        TeamM = self.env ["teamm"]
        kwargs = {
            "name": self._teamm2odoo_name(),
            "date_begin": TeamM._get_date("from"),
            "date_end": TeamM._get_date("to"),
        }
        records = self._teamm2odoo_set_record(kwargs)
        return records

    @api.model
    def _teamm2odoo_values(self, kwargs):
        kwargs |= {
            "resource_booking_id": self.env["resource.booking"]._teamm2odoo_search()
        }
        return super()._teamm2odoo_values(kwargs)
