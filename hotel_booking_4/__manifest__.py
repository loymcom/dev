{
    "name": "Hotel Booking",
    "version": "1.0",
    "summary": "Module Summary",
    "description": "Module Description",
    "category": "Administration",
    "author": "Rick, Henrik",
    "website": "Author Website",
    "depends": [
        "booking_view",
        "hotel",
    ],
    "data": [
        "data/default_hotel_room_type.xml",
        "views/hotel_floor_view.xml",
        "views/hotel_folio_view.xml",
        "views/hotel_room_view.xml",
    ],
    "license": "LGPL-3",
    'assets': {
        'web.assets_backend': [
            'hotel_booking_4/static/src/**/*',
            'hotel_booking_4/static/tests/**/*',
            ('remove', 'hotel_booking_4/static/src/dashboard/**/*'),
        ],
        'hotel_booking.dashboard': [
            # To include bootstrap scss variables
            ("include", 'web._assets_helpers'), 
            ('include', 'web._assets_backend_helpers'),
            'hotel_booking_4/static/src/dashboard/**/*',
        ],
        'web.order_tests': [
            ("include", 'web.assets_frontend'), 
            'hotel_booking_4/static/tests/**/*',
        ],
    }
}
