import pytz
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
        booking_periods = self.product_id.booking_period_ids
        if booking_periods:
            for result_date, result_dts in result.items():
                new_dts = []
                for result_dt in result_dts:
                    start = result_dt.astimezone(pytz.utc).replace(tzinfo=None)
                    stop = start + timedelta(hours=self.duration)
                    for period in booking_periods:
                        if period.start <= start < period.stop and period.start < stop <= period.stop:
                            new_dts.append(result_dt)
                result[result_date] = new_dts
        return result

    def action_bookings_this_period(self):
        bookings_this_period = self._get_bookings_this_period()
        return {
            "name": "Bookings",
            "type": "ir.actions.act_window",
            "res_model": "resource.booking",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", bookings_this_period.ids]],
        }

    def action_contacts_this_period(self):
        contacts_this_period = self._get_bookings_this_period().mapped("partner_ids")
        return {
            "name": "Contacts",
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "views": [
                [
                    self.env.ref("sale_resource_booking_period.view_partner_tree").id,
                    "tree",
                ],
                [False, "form"],
            ],
            "domain": [["id", "in", contacts_this_period.ids]],
            "context": {"resource_booking_period_id": self.id},
        }

    def _get_bookings_this_period(self):
        return self.search([
            ("type_id", "!=", self.type_id.id),
            "|",
            "&", ("start", ">", self.start),("start", "<", self.stop),
            "&", ("stop", ">", self.start),("stop", "<", self.stop),
        ])
