# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

# Copied from pos.config
class HotelFolio(models.Model):
    # _name = 'hotel.folio'
    # _inherit = ['hotel.folio', 'pos.config']

    _inherit = "hotel.folio"

    def open_ui_2(self):
        return self._action_to_open_ui()
    
    def _action_to_open_ui(self):
        path = "/floor/ui"
        return {
            'type': 'ir.actions.act_url',
            'url': path + '?hotel_folio_id=%d' % self.id,
            'target': 'self',
        }
