from odoo import api, fields, models, tools
from odoo.addons.resource_booking.models.resource_booking import _availability_is_fitting


class ResourceBookingAvailability(models.Model):
    _name = "resource.booking.availability"
    _description = "resource.booking.availability"
    _auto = False

    # Stored fields
    session_id = fields.Many2one("resource.booking.session")
    product_tmpl_id = fields.Many2one("product.template")
    product_id = fields.Many2one("product.product")
    booking_type_id = fields.Many2one("resource.booking.type")
    # Computed fields
    pav_ids = fields.Many2many(
        "product.attribute.value",
        relation="resource_booking_type_product_attribute_value_rel",
        related="booking_type_id.product_attribute_value_ids",
    )
    pav_tag_ids = fields.Many2many(
        "product.attribute.value.tag",
        compute="_compute_pav_tag_ids",
    )
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
                start = fields.Datetime.context_timestamp(self, rec.session_id.start)
                stop = fields.Datetime.context_timestamp(self, rec.session_id.stop)
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
                rbs.id::text || '_' || pp.id::text AS id,
                rbs.id AS session_id,
                pt.id AS product_tmpl_id,
                pp.id AS product_id,
                rbt.id AS booking_type_id
            FROM resource_booking_session_for_product_template_rel rbs_pt
            JOIN resource_booking_session rbs ON rbs_pt.resource_booking_session_id = rbs.id
            JOIN product_template pt ON rbs_pt.product_template_id = pt.id
            JOIN product_product pp ON pp.product_tmpl_id = pt.id
            JOIN resource_booking_type rbt ON pp.resource_booking_type_id = rbt.id
            """
        )
