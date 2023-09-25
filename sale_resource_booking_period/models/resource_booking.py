import pytz
from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    period_product_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        relation="resource_booking_period_for_product_template_rel",
        string="Period Products",
    )

    def _get_available_slots(self, start_dt, end_dt):
        result = super()._get_available_slots(start_dt, end_dt)
        # If the product has booking periods,
        # then restrict to these periods.
        # dt = datetime
        # dts = list of datetimes
        booking_periods = self.product_id.booking_period_ids
        if booking_periods:
            new_result = defaultdict(list)
            for result_date, result_dts in result.items():
                new_dts = []
                for result_dt in result_dts:
                    start = result_dt.astimezone(pytz.utc).replace(tzinfo=None)
                    stop = start + timedelta(hours=self.duration)
                    for period in booking_periods:
                        if period.start <= start < period.stop and period.start < stop <= period.stop:
                            new_result[result_date].append(result_dt)
            result = new_result
        return result
