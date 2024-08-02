from collections import defaultdict

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    def _compute_resource_booking_combination_ids(self):
        # Session -> Contacts -> Combinations in this session
        session_id = self.env.context.get("resource_booking_session_id")
        if session_id:
            session = self.env["resource.booking"].browse(session_id)
            bookings = session._get_bookings_this_session()
            combinations = defaultdict(list)
            for booking in bookings:
                for partner in booking.partner_ids:
                    combinations[partner.id].append(booking.combination_id.id)
            for partner in self:
                partner.resource_booking_combination_ids = combinations[partner.id]
        else:
            self.resource_booking_combination_ids = None

    resource_booking_combination_ids = fields.Many2many(
        "resource.booking.combination",
        string="Booking Combination",
        compute="_compute_resource_booking_combination_ids",
    )
