# Copyright 2023 Ows - Henrik Norlin
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stripe Subscriptions",
    "summary": "",
    "author": "Ows, Odoo Community Association (OCA)",
    "category": "Accounting/Payment Providers",
    "data": [
        "views/templates.xml",
    ],
    "depends": [
        "payment_stripe",
    ],
    "development_status": "Alpha",
    "license": "AGPL-3",
    "maintainers": ["ows-cloud"],
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/",
    'assets': {
        'payment_stripe_subscription.test': [
            'payment_stripe_subscription/static/src/popper/*',
            # 'payment_stripe_subscription/static/src/bootstrap/**/*',
            'payment_stripe_subscription/static/src/bootstrap/js/bootstrap.bundle.min.js',
            'payment_stripe_subscription/static/src/bootstrap/css/bootstrap.min.css',
        ],
        'payment_stripe_subscription.test_1': [
            # bootstrap
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap'),

            'web/static/src/libs/fontawesome/css/font-awesome.css', # required for fa icons
            'web/static/src/legacy/js/promise_extension.js', # required by boot.js
            'web/static/src/boot.js', # odoo module system
            'web/static/src/env.js', # required for services
            'web/static/src/session.js', # expose __session_info__ containing server information
            'web/static/lib/owl/owl.js', # owl library
            'web/static/lib/owl/odoo_module.js', # to be able to import "@odoo/owl"
            'web/static/src/core/utils/functions.js',
            'web/static/src/core/browser/browser.js',
            'web/static/src/core/registry.js',
            'web/static/src/core/assets.js',
            # 'owl_playground/static/src/**/*',
        ],
    }
}
