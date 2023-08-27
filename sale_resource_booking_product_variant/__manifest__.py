# Copyright 2023 AppsToGROW - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sell Product Variants with Resources",
    "summary": "",
    "author": "AppsToGROW, Odoo Community Association (OCA)",
    "category": "Uncategorized",
    "data": [
        "views/product_attribute_views.xml",
        "views/menus.xml",
    ],
    "depends": [
        "sale_resource_booking",
    ],
    "development_status": "Alpha",
    "license": "AGPL-3",
    "maintainers": ["appstogrow"],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "version": "14.0.1.0.0",
    "website": "https://github.com/appstogrow/apps",
}
