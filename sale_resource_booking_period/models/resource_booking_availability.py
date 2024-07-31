import pytz
from collections import defaultdict
from datetime import timedelta

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.addons.resource.models.resource import Intervals
from odoo.addons.resource_booking.models.resource_booking import _availability_is_fitting


class ResourceBookingAvailability(models.Model):
    _name = "resource.booking.availability"
    _description = "resource.booking.availability"
    _auto = False

    # Stored fields
    period_id = fields.Many2one("resource.booking", help="period_type='period'")
    product_tmpl_id = fields.Many2one("product.template")
    booking_type_id = fields.Many2one("resource.booking.type")
    # Computed fields
    pav_ids = fields.Many2many(
        "product.attribute.value",
        relation="resource_booking_type_product_attribute_value_rel",
        related="booking_type_id.product_attribute_value_ids",
    )
    pav_tag_ids = fields.Many2many(
        "product.attribute.value.tag",
        # relation="product_attribute_value_tag_rel",
        # related="booking_type_id.product_attribute_value_ids.tag_ids",
        compute="_compute_pav_tag_ids",
    )
    combination_rel_ids = fields.One2many(
        "resource.booking.type.combination.rel",
        related="booking_type_id.combination_rel_ids",
    )
    # combination_ids = fields.Many2one(
    #     "resource.booking.combination",
    #     related="booking_type_id.combination_rel_ids.combination_id",
    # )
    available_ids = fields.Many2many(
        "resource.booking.combination",
        compute="_compute_available_ids",
        store=False,
    )

    def _compute_pav_tag_ids(self):
        for record in self:
            pav_ids = record.pav_ids
            record.pav_tag_ids = pav_ids.tag_ids

    def _compute_available_ids(self):
        for rec in self:
            ids = []
            for combination in rec.booking_type_id.combination_rel_ids.combination_id:
                Booking = self.env["resource.booking"]
                start = fields.Datetime.context_timestamp(self, rec.period_id.start)
                stop = fields.Datetime.context_timestamp(self, rec.period_id.stop)
                available_intervals = Booking._get_intervals(
                    start, stop, combination, rec.booking_type_id
                )
                if _availability_is_fitting(available_intervals, start, stop):
                    ids.append(combination.id)
            rec.available_ids = ids

    def init(self):
        tools.drop_view_if_exists(self._cr, "resource_booking_availability")
        # In case of bad performance,
        # add "location" field to product_template & resource_booking_type and JOIN them
        self._cr.execute(
            """
        CREATE OR REPLACE VIEW resource_booking_availability AS
        SELECT DISTINCT
        rbp.id::text || '_' || pt.id::text || '_' || rbt.id::text AS id,
        rbp.id AS period_id,
        pt.id AS product_tmpl_id,
        rbt.id AS booking_type_id
        FROM resource_booking_period_for_product_template_rel rbp_pt
        JOIN resource_booking rbp ON rbp_pt.resource_booking_id = rbp.id
        JOIN product_template pt ON rbp_pt.product_template_id = pt.id
            JOIN product_template_attribute_value ptav ON ptav.product_tmpl_id = pt.id
            JOIN product_attribute_value pav ON ptav.product_attribute_value_id = pav.id
            JOIN resource_booking_type_product_attribute_value_rel rbt_pav
                ON rbt_pav.product_attribute_value_id = pav.id
        JOIN resource_booking_type rbt ON rbt_pav.resource_booking_type_id = rbt.id
            """
        )
