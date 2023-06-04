# Copyright 2023 Fredheim - Henrik Norlin
# Copyright 2023 Fredheim - Rick Neubrander
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Variant Resource Booking",
    "summary": "",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Appointments",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Fredheim, Odoo Community Association (OCA)",
    "maintainers": ["neuby001", "norlinhenrik"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "date_range",
        "product",
        "resource_booking",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
        "views/resource_resource_views.xml",
        "wizard/product_variant_resource_booking_views.xml",
    ],
}
