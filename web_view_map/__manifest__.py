{
    'name': "Map View",
    'summary': "Rectangle / Image / Map",
    'description': """
        Place items in a rectangle or image or map. Inspired by pos_restaurant FloorScreen.
    """,
    'license': 'LGPL-3',
    'version': '0.1',
    'depends': ['web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'web_view_map/static/src/**/*',
            # 'web_view_map/static/src/*',  # without MapScreen
        ],
    },
}
