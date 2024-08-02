from odoo import api, fields, models


class ResourceBookingSession(models.Model):
    _name = "resource.booking.session"
    _inherits = {"resource.booking": "booking_id"}
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]

    booking_id = fields.Many2one("resource.booking")

    session_booking_count = fields.Integer(
        "Bookings",
        compute="_compute_session",
    )
    session_partner_count = fields.Integer(
        "Contacts",
        compute="_compute_session",
    )

    def _compute_session(self):
        for session in self:
            session.session_booking_count = len(session._get_bookings_this_session())
            session.session_partner_count = len(
                session._get_bookings_this_session().mapped("partner_ids")
            )

    def action_bookings_this_session(self):
        bookings_this_session = self._get_bookings_this_session()
        return {
            "name": "Bookings",
            "type": "ir.actions.act_window",
            "res_model": "resource.booking",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", bookings_this_session.ids]],
        }

    def action_contacts_this_session(self):
        contacts_this_session = self._get_bookings_this_session().mapped("partner_ids")
        partner_view = "resource_booking_session.view_partner_tree"
        return {
            "name": "Contacts",
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "views": [
                [self.env.ref(partner_view).id, "tree"],
                [False, "form"],
            ],
            "domain": [["id", "in", contacts_this_session.ids]],
            "context": {"resource_booking_session_id": self.id},
        }

    def _get_bookings_this_session(self):
        return self.search([
            "|",
            "&", ("start", ">", self.start),("start", "<", self.stop),
            "&", ("stop", ">", self.start),("stop", "<", self.stop),
        ])
