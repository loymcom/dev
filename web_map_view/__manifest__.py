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
            'web_map_view/static/src/**/*',
            # 'web_map_view/static/src/*',  # without MapScreen
        ],
    },
}
