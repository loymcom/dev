import pytz
from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, tools


class ResourceBookingAvailability(models.Model):
    _name = "resource.booking.availability"
    _description = "resource.booking.availability"
    _auto = False

    period_id = fields.Many2one("resource.booking", help="period_type='period'")
    product_tmpl_id = fields.Many2one("product.template")
    # product_attr_ids = fields.Many2one("product.attribute")
    # product_attr_value_ids = fields.Many2one("product.attribute.value")
    booking_type_id = fields.Many2one("resource.booking.type")
    product_attr_value_id = fields.Many2one(
        "product.attribute.value",
        # related="booking_type_id.product_attribute_value_ids",
    )
    # product_attr_value_ids = fields.Many2one(
    #     "product.attribute.value",
    #     related="booking_type_id.product_attribute_value_ids",
    # )

    def init(self):
        tools.drop_view_if_exists(self._cr, "resource_booking_availability")
        self._cr.execute(
            """
            CREATE OR REPLACE VIEW resource_booking_availability AS
            SELECT DISTINCT
                rbp.id::text || '_' || pt.id::text || '_' || pav.id::text || '_' || rbt.id::text AS id,
                --pp.id AS product_id,
                rbp.id AS period_id,
                pt.id AS product_tmpl_id,
                pav.id AS product_attr_value_id,
                --pa.id AS product_attr_id,
                rbt.id AS booking_type_id
            FROM resource_booking_period_for_product_template_rel rbp_pt
            JOIN resource_booking rbp ON rbp_pt.resource_booking_id = rbp.id
            JOIN product_template pt ON rbp_pt.product_template_id = pt.id
            --JOIN product_product pp ON pp.product_tmpl_id = pt.id
            JOIN product_template_attribute_value ptav ON ptav.product_tmpl_id = pt.id
            JOIN product_attribute_value pav ON ptav.product_attribute_value_id = pav.id
            JOIN product_attribute pa ON pav.attribute_id = pa.id
            --JOIN resource_booking_type_product_attribute_value_rel rbt_pav
            JOIN product_attribute_value_resource_booking_type_rel rbt_pav
                ON rbt_pav.product_attribute_value_id = pav.id
            JOIN resource_booking_type rbt ON rbt_pav.resource_booking_type_id = rbt.id
            """
        )
