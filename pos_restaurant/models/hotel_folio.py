# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

# Copied from pos.config
class HotelFolio(models.Model):
    _name = 'hotel.folio'
    _inherit = ['hotel.folio', 'pos.config']

    # printer_ids = fields.Many2many('restaurant.printer', 'pos_config_printer_rel', 'config_id', 'printer_id', string='Order Printers')


    # _inherits = {'pos.config': 'pos_config_id'}

    # pos_config_id = fields.Many2one('pos.config', string='Point of Sale')
