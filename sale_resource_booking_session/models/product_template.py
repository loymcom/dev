from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    booking_session_ids = fields.Many2many(
        comodel_name="resource.booking.session",
        relation="resource_booking_session_for_product_template_rel",
        string="Booking Sessions",
    )
