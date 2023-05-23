{
    'name': "Booking View",
    'summary': "Defines the 'booking' view",
    'description': """
        Defines a new type of view ('booking_view') which allows to book a room.
    """,

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
            'booking_view/static/src/**/*',
        ],
    },
    'license': 'AGPL-3'
}
