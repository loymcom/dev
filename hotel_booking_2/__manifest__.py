{
    "name": "Hotel Booking",
    "version": "1.0",
    "summary": "Module Summary",
    "description": "Module Description",
    "category": "Administration",
    "author": "Rick, Henrik",
    "website": "Author Website",
    "depends": [
        "hotel",
        # "pos_restaurant",
    ],
    "data": [
        "data/default_hotel_room_type.xml",
        "views/hotel_floor_view.xml",
        "views/hotel_folio_view.xml",
        "views/hotel_room_view.xml",
        'views/template.xml',
    ],
    "license": "LGPL-3",
    'assets': {
        'hotel_booking_2.assets_playground': [
            # bootstrap
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap'),

            'web/static/src/libs/fontawesome/css/font-awesome.css', # required for fa icons
            'web/static/src/legacy/js/promise_extension.js', # required by boot.js
            'web/static/src/boot.js', # odoo module system
            'web/static/src/env.js', # required for services
            'web/static/src/session.js', # expose __session_info__ containing server information
            'web/static/lib/owl/owl.js', # owl library
            'web/static/lib/owl/odoo_module.js', # to be able to import "@odoo/owl"
            'web/static/src/core/utils/functions.js',
            'web/static/src/core/browser/browser.js',
            'web/static/src/core/registry.js',
            'web/static/src/core/assets.js',

            # FloorScreen DEPENDENCIES
            "web/static/src/legacy/legacy_component.js",  # PosComponent
            "hotel_booking_2/static/src/js/point_of_sale/PosComponent.js",  # FloorScreen, ComponentRegistry

            "hotel_booking_2/static/src/js/point_of_sale/ClassRegistry.js",  # Registries, ComponentRegistry
            "hotel_booking_2/static/src/js/point_of_sale/ComponentRegistry.js",  # Registries
            "hotel_booking_2/static/src/js/point_of_sale/Registries.js",  # FloorScreen

            "web/static/src/core/browser/browser.js",  # timing, rpc_service
            "web/static/src/core/utils/timing.js",  # FloorScreen

            "web/static/src/core/utils/hooks.js",  # EditableTable

            "web/static/src/core/registry.js",  # rpc_service
            "web/static/src/core/network/rpc_service.js", # utils
            "hotel_booking_2/static/src/js/point_of_sale/utils.js",  # FloorScreen

            # "pos_restaurant/static/src/js/Screens/FloorScreen/FloorScreen.js",  # hotel.room hotel.floor hotel.folio
            # _save(table)         restaurant.table hotel.room create_from_ui([tableCopy])
            # _tableLongpolling()        pos.config hotel.folio get_tables_order_count([this.env.pos.config.id])
            # setFloorColor(color) restaurant.floor hotel.floor write([this.activeFloor.id], { background_color: color })
            # deleteTable()        restaurant.table hotel.room create_from_ui([{ active: false, id: originalSelectedTableId }])
            'hotel_booking_2/static/src/**/*',
        ],
    },
}
