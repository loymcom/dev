import pytz
from datetime import timedelta

from odoo import api, fields, models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    period_type = fields.Selection(
        [
            ("period", "Period"),
            ("statistics", "Include in Period Statistics"),
        ],
        string="Period Type",
        related="type_id.period_type",
        readonly=True,
    )

    period_booking_count = fields.Integer(
        "Bookings",
        compute="_compute_period",
    )
    period_partner_count = fields.Integer(
        "Contacts",
        compute="_compute_period",
    )
    # parent_id = fields.Many2one(
    #     "resource.booking",
    #     string="Related Booking",
    # )

    def _compute_period(self):
        for period in self:
            period.period_booking_count = len(period._get_bookings_this_period())
            period.period_partner_count = len(
                period._get_bookings_this_period().mapped("partner_ids")
            )

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
                    self.env.ref("resource_booking_period.view_partner_tree").id,
                    "tree",
                ],
                [False, "form"],
            ],
            "domain": [["id", "in", contacts_this_period.ids]],
            "context": {"resource_booking_period_id": self.id},
        }

    def _get_bookings_this_period(self):
        return self.search([
            ("type_id.period_type", "=", "statistics"),
            "|",
            "&", ("start", ">", self.start),("start", "<", self.stop),
            "&", ("stop", ">", self.start),("stop", "<", self.stop),
        ])
