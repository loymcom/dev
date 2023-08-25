from odoo import api, fields, models


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    product_id = fields.Many2one("product.product", string="Product Variant")
    date_range_id = fields.Many2one("date.range", string="Date Range")

    def action_sale_order_wizard(self):
        """Help user creating a sale order for this RBT."""
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "sale_resource_booking.resource_booking_sale_action"
        )
        result["context"] = dict(
            self.env.context,
            default_type_id=self.type_id.id,
            default_partner_id=self.partner_id.id,
            default_product_id=self.product_id.id,
            default_date_range_id=self.date_range_id.id,
        )
        return result
