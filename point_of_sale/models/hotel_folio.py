# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

# Copied from pos.config
class HotelFolio(models.Model):
    _name = 'hotel.folio'
    _inherit = ['hotel.folio', 'pos.config']
