from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    hotel_folio_count = fields.Integer(compute='_compute_hotel_folio_count', string='Hotel Folio Count')
    hotel_folio_ids = fields.One2many('hotel.folio', 'partner_id', 'Hotel Folio')

    def action_view_hotel_folio(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "res_model": "hotel.folio",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [("partner_id", "in", self.id)],
            "context": {'default_partner_id': self.id},
        }
        return action

    def _compute_hotel_folio_count(self):
        for record in self:
            record.hotel_folio_count = len(record.hotel_folio_ids)
