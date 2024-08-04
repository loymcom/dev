# Copyright 2024 Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Online Events with Resource Booking",
    "summary": "",
    "author": "Henrik Norlin, Odoo Community Association (OCA)",
    "category": "Appointments",
    "data": [
        "security/ir.model.access.csv",
        # "views/resource_booking_availability_views.xml",
    ],
    "depends": [
        # "product_attribute_value_tag",
        "event_sale_resource_booking",
        "website_sale_product_variant",
        # "website_sale_resource_booking",
    ],
    "auto_install": True,
    "license": "AGPL-3",
    "maintainers": ["norlinhenrik"],
    "post_init_hook": "post_init_hook",
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/",
}
