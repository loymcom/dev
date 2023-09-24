from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    booking_period_ids = fields.Many2many(
        comodel_name="resource.booking",
        relation="resource_booking_period_for_product_template_rel",
        string="Booking Periods",
        domain="[('type_id.period_type', '=', 'period')]",
    )
