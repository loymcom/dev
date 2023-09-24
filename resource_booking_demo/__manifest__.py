# Copyright 2023 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Resource Booking Demo",
    "summary": "",
    "author": "Ows, Odoo Community Association (OCA)",
    "category": "Uncategorized",
    "data": [
        "demo/demo.xml",
        "views/resource_booking_views.xml",
    ],
    "depends": [
        "contacts",
        "hr",
        "payment_demo",  # or payment_custom
        "sale_management",
        "website_sale_resource_booking",  # oca/calendar, oca/sale-workflow, oca/e-commerce
        "partner_product_price",  # oca/product-attribute
        "resource_booking_timeline",
        "sale_resource_booking_product_variant",
        "sale_resource_booking_period",
    ],
    "development_status": "Alpha",
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/",
}
