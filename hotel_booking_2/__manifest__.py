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
        "pos_restaurant",
    ],
    "data": [
        "data/default_hotel_room_type.xml",
        'views/floor_assets_index.xml',
        "views/hotel_floor_view.xml",
        "views/hotel_folio_view.xml",
        "views/hotel_room_view.xml",
    ],
    "license": "LGPL-3",
    # 'assets': {
    #     'point_of_sale.assets': [
    #         'hotel_booking/static/lib/**/*.js',
    #         'hotel_booking/static/src/js/**/*.js',
    #         ('after', 'point_of_sale/static/src/scss/pos.scss', 'hotel_booking/static/src/scss/restaurant.scss'),
    #         'hotel_booking/static/src/xml/**/*',
    #     ],
    #     'web.assets_backend': [
    #         'point_of_sale/static/src/scss/pos_dashboard.scss',
    #     ],
    #     'web.assets_tests': [
    #         'hotel_booking/static/tests/tours/**/*',
    #     ],
    # },
}
