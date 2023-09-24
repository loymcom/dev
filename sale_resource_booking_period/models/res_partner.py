from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    def _compute_resource_booking_combination_id(self):
        period_id = self.env.context.get("resource_booking_period_id")
        if period_id:
            period = self.env["resource.booking"].browse(period_id)
            bookings = period._get_bookings_this_period()
            partner_booking = {
                p.id: b.combination_id.id for b in bookings for p in b.partner_ids
            }
            for partner in self:
                partner.resource_booking_combination_id = partner_booking[partner.id]
        else:
            self.resource_booking_combination_id = None

    resource_booking_combination_id = fields.Many2one(
        "resource.booking.combination",
        compute="_compute_resource_booking_combination_id",
    )
