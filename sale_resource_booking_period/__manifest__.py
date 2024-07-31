# Copyright 2023 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sell Resource Booking Periods",
    "summary": "",
    "author": "Ows, Odoo Community Association (OCA)",
    "category": "Appointments",
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/resource_booking_availability_views.xml",
        "views/resource_booking_views.xml",
    ],
    "depends": [
        "product_attribute_value_tag",
        "resource_booking_period",
        "sale_resource_booking",  # with booking.product_id
    ],
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/sale-workflow",
}
