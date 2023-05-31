{
    "name": "Hotel Floor Map",
    "version": "1.0",
    "summary": "Module Summary",
    "description": "Module Description",
    "category": "Administration",
    "author": "Rick, Henrik",
    "website": "Author Website",
    "depends": [
        "awesome_gallery",  # TODO: When web_map_view is finished, remove all instances of "gallery" in the code.
        "hotel",
        "web_view_map",
    ],
    "data": [
        "data/default_hotel_room_type.xml",
        "security/ir.model.access.csv",
        "views/hotel_floor_views.xml",
        "views/hotel_folio_views.xml",
        "views/hotel_room_views.xml",
        "views/hotel_session_views.xml",
        "views/res_partner_views.xml",
    ],
    "license": "AGPL-3",
}
