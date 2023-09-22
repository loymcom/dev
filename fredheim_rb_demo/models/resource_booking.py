from odoo import api, fields, models

class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    @api.depends("partner_id")
    def _compute_partner_ids(self):
        for record in self:
            if record.partner_id:
                record.partner_ids = [(6, 0, [self.partner_id.id])]

    def _inverse_partner_ids(self):
        pass

    partner_ids = fields.Many2many(
        "res.partner",
        string="Contacts",
        store=True,
        compute="_compute_partner_ids",
        inverse="_inverse_partner_ids",
    )

    def action_save(self):
        pass

    def action_bookings_this_interval(self):
        bookings_this_interval = self.search([
            ("type_id", "!=", self.type_id.id),
            "|",
            "&", ("start", ">", self.start),("start", "<", self.stop),
            "&", ("stop", ">", self.start),("stop", "<", self.stop),
        ])
        return {
            "name": "Bookings",
            "type": "ir.actions.act_window",
            "res_model": "resource.booking",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", bookings_this_interval.ids]],
        }

    def action_contacts_this_interval(self):
        contacts_this_interval = self.search([
            "|",
            ("start", "<", self.stop),
            ("stop", ">", self.start),
        ]).mapped("partner_ids")
        return {
            "name": "Contacts",
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", contacts_this_interval.ids]],
        }
