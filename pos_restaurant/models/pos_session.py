# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from itertools import groupby
from odoo.osv.expression import AND

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if self.config_id.module_pos_restaurant:
            # result.append('restaurant.printer')
            if self.config_id.is_table_management:
                result.append('hotel.folio')
                result.append('hotel.floor')
                result.append('restaurant.floor')
        return result

    def _loader_params_hotel_floor(self):
        return {
            'search_params': {
                'domain': [('pos_config_id', '=', self.config_id.id)],
                'fields': ['name', 'background_color', 'table_ids', 'sequence'],
                'order': 'sequence',
            },
        }

    def _loader_params_restaurant_floor(self):
        return {
            'search_params': {
                'domain': [('pos_config_id', '=', self.config_id.id)],
                'fields': ['name', 'background_color', 'table_ids', 'sequence'],
                'order': 'sequence',
            },
        }

    def _loader_params_hotel_room(self):
        return {
            'search_params': {
                'domain': [('active', '=', True)],
                'fields': [
                    'name', 'width', 'height', 'position_h', 'position_v',
                    'shape', 'floor_id', 'color', 'seats', 'active'
                ],
            },
        }

    def _get_pos_ui_hotel_floor(self, params):
        floors = self.env['hotel.floor'].search_read(**params['search_params'])
        floor_ids = [floor['id'] for floor in floors]

        table_params = self._loader_params_hotel_room()
        table_params['search_params']['domain'] = AND([table_params['search_params']['domain'], [('floor_id', 'in', floor_ids)]])
        tables = self.env['hotel.room'].search(table_params['search_params']['domain'], order='floor_id')
        tables_by_floor_id = {}
        for floor_id, table_group in groupby(tables, key=lambda table: table.floor_id):
            floor_tables = self.env['hotel.room'].concat(*table_group)
            tables_by_floor_id[floor_id.id] = floor_tables.read(table_params['search_params']['fields'])

        for floor in floors:
            floor['tables'] = tables_by_floor_id.get(floor['id'], [])

        return floors

    def _get_pos_ui_restaurant_floor(self, params):
        floors = self.env['restaurant.floor'].search_read(**params['search_params'])
        floor_ids = [floor['id'] for floor in floors]

        table_params = self._loader_params_hotel_room()
        table_params['search_params']['domain'] = AND([table_params['search_params']['domain'], [('floor_id', 'in', floor_ids)]])
        tables = self.env['restaurant.table'].search(table_params['search_params']['domain'], order='floor_id')
        tables_by_floor_id = {}
        for floor_id, table_group in groupby(tables, key=lambda table: table.floor_id):
            floor_tables = self.env['restaurant.table'].concat(*table_group)
            tables_by_floor_id[floor_id.id] = floor_tables.read(table_params['search_params']['fields'])

        for floor in floors:
            floor['tables'] = tables_by_floor_id.get(floor['id'], [])

        return floors

    def _loader_params_hotel_folio(self):
        return {'search_params': {'domain': [('id', '=', self.config_id.id)], 'fields': []}}

    def _get_pos_ui_hotel_folio(self, params):
        config = self.env['hotel.folio'].search_read(**params['search_params'])[0]
        config['use_proxy'] = config['is_posbox'] and (config['iface_electronic_scale'] or config['iface_print_via_proxy']
                                                       or config['iface_scan_via_proxy'] or config['iface_customer_facing_display_via_proxy'])
        return config

    # def _loader_params_restaurant_printer(self):
    #     return {
    #         'search_params': {
    #             'domain': [('id', 'in', self.config_id.printer_ids.ids)],
    #             'fields': ['name', 'proxy_ip', 'product_categories_ids', 'printer_type'],
    #         },
    #     }
    # def _get_pos_ui_restaurant_printer(self, params):
    #     return self.env['restaurant.printer'].search_read(**params['search_params'])

    def close_session_from_ui(self, bank_payment_method_diff_pairs=None):
        """Calling this method will try to close the session.

        param bank_payment_method_diff_pairs: list[(int, float)]
            Pairs of payment_method_id and diff_amount which will be used to post
            loss/profit when closing the session.

        If successful, it returns {'successful': True}
        Otherwise, it returns {'successful': False, 'message': str, 'redirect': bool}.
        'redirect' is a boolean used to know whether we redirect the user to the back end or not.
        When necessary, error (i.e. UserError, AccessError) is raised which should redirect the user to the back end.
        """
        bank_payment_method_diffs = dict(bank_payment_method_diff_pairs or [])
        self.ensure_one()
        # Even if this is called in `post_closing_cash_details`, we need to call this here too for case
        # where cash_control = False
        check_closing_session = self._cannot_close_session(bank_payment_method_diffs)
        if check_closing_session:
            return check_closing_session

        validate_result = self.action_pos_session_closing_control(bank_payment_method_diffs=bank_payment_method_diffs)

        # If an error is raised, the user will still be redirected to the back end to manually close the session.
        # If the return result is a dict, this means that normally we have a redirection or a wizard => we redirect the user
        if isinstance(validate_result, dict):
            # imbalance accounting entry
            return {
                'successful': False,
                'message': validate_result.get('name'),
                'redirect': True
            }

        self.message_post(body='Point of Sale Session ended')

        return {'successful': True}
