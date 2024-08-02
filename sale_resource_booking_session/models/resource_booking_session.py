import pytz
from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models


class ResourceBookingSession(models.Model):
    _inherit = "resource.booking.session"

    product_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        relation="resource_booking_session_for_product_template_rel",
        string="Session Products",
    )
