from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _compute_hotel_folio_count(self):
        for record in self:
            record.hotel_folio_count = len(record.hotel_folio_ids)

    hotel_folio_count = fields.Integer(compute='_compute_hotel_folio_count', string='Hotel Folio Count')
    hotel_folio_ids = fields.One2many('hotel.folio', 'partner_id', 'Hotel Folio')

    def action_view_partner_folios(self):
        self.ensure_one()
        return {
            "name": "Folios",
            "type": "ir.actions.act_window",
            "res_model": "hotel.folio",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [("partner_id.id", "=", self.id)],
            "context": {'default_partner_id': self.id},
        }


