import pytz
from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    def _get_available_slots(self, start_dt, end_dt):
        result = super()._get_available_slots(start_dt, end_dt)
        # If the product has booking sessions,
        # then restrict to these sessions.
        # dt = datetime
        # dts = list of datetimes
        booking_sessions = self.product_id.booking_session_ids
        if booking_sessions:
            new_result = defaultdict(list)
            for result_date, result_dts in result.items():
                new_dts = []
                for result_dt in result_dts:
                    start = result_dt.astimezone(pytz.utc).replace(tzinfo=None)
                    stop = start + timedelta(hours=self.duration)
                    for session in booking_sessions:
                        if session.start <= start < session.stop and session.start < stop <= session.stop:
                            new_result[result_date].append(result_dt)
            result = new_result
        return result
