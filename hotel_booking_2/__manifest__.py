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
        "point_of_sale",
    ],
    "data": [
        "data/hotel_room_type_data.xml",
        "views/hotel_floor_views.xml",
        "views/hotel_room_views.xml",
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
