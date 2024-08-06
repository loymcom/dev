from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    websites = env["website"].search([])
    websites.shop_model = "event.booking.combination"
