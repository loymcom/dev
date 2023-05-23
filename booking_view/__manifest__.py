{
    'name': "Booking View",
    'summary': "Defines the 'booking' view",
    'description': """
        Defines a new type of view ('booking_view') which allows to book a room.
    """,
    'license': 'LGPL-3',
    'version': '0.1',
    'depends': ['hotel'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            # 0: "@web/../tests/helpers/cleanup"
            # 1: "@web/../tests/helpers/mock_env"
            # 2: "@web/../tests/search/helpers"
            # 3: "@web/../tests/webclient/helpers"
            # 4: "@web/../tests/helpers/mock_services"
            # 5: "web.test_env"
            # 'web/static/tests/helpers/utils.js',
            # 'web/static/tests/views/helpers.js',
            # 'booking_view/static/tests/**/*',

            # FloorScreen DEPENDENCIES
            "web/static/src/webclient/webclient.xml",
            # "web/static/src/legacy/legacy_component.js",  # PosComponent
            "booking_view/static/src/FloorScreen/point_of_sale/PosComponent.js",  # FloorScreen, ComponentRegistry

            "booking_view/static/src/FloorScreen/point_of_sale/ClassRegistry.js",  # Registries, ComponentRegistry
            "booking_view/static/src/FloorScreen/point_of_sale/ComponentRegistry.js",  # Registries
            "booking_view/static/src/FloorScreen/point_of_sale/Registries.js",  # FloorScreen

            "web/static/src/core/browser/browser.js",  # timing, rpc_service
            "web/static/src/core/utils/timing.js",  # FloorScreen

            "web/static/src/core/utils/hooks.js",  # EditableTable

            "web/static/src/core/registry.js",  # rpc_service
            "web/static/src/core/network/rpc_service.js", # utils
            "booking_view/static/src/FloorScreen/point_of_sale/utils.js",  # FloorScreen

            "booking_view/static/src/FloorScreen/FloorScreen.js",  # hotel.room hotel.floor hotel.folio

            'booking_view/static/src/**/*',
        ],
    },
}
