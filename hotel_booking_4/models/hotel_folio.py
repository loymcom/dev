from itertools import groupby

from odoo import api, fields, models, _
from odoo.osv.expression import AND


class HotelFolio(models.Model):
    _inherit = "hotel.folio"

    #
    # Inspired by pos.config
    #

    def open_ui_2(self):
        return self._action_to_open_ui()
    
    def _action_to_open_ui(self):
        path = "/hotel_booking/ui"
        return {
            'type': 'ir.actions.act_url',
            'url': path + '?hotel_folio_id=%d' % self.id,
            'target': 'self',
        }
    
    #
    # Inspired by pos.session
    #

    def load_booking_data(self):
        loaded_data = {}
        self = self.with_context(loaded_data=loaded_data)
        for model in self._booking_ui_models_to_load():
            loaded_data[model] = self._load_model(model)
        # self._pos_data_process(loaded_data)

        # keys = [key for key, value in loaded_data.items()]
        # keys.sort()
        # for key in keys:
        #     _logger.warning("{}".format(key))
        return loaded_data

    @api.model
    def _booking_ui_models_to_load(self):
        models_to_load = [
            "hotel.floor",
            # "hotel.room",
            # 'res.company',
            # 'res.lang',
            # 'res.users',
        ]
        return models_to_load

    def _load_model(self, model):
        model_name = model.replace('.', '_')
        loader = getattr(self, '_get_booking_ui_%s' % model_name, None)
        params = getattr(self, '_loader_params_%s' % model_name, None)
        if loader and params:
            return loader(params())
        else:
            raise NotImplementedError(_("The function to load %s has not been implemented.", model))

    def _loader_params_hotel_floor(self):
        return {
            'search_params': {
                'domain': [],
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
