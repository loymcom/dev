import logging

from collections import defaultdict
from datetime import datetime

from odoo import api, fields, models, tools
from odoo.addons.resource_booking.models.resource_booking import _availability_is_fitting

_logger = logging.getLogger(__name__)


class EventBookingCombination(models.Model):
    _name = "event.booking.combination"
    _description = "event.booking.combination"
    _auto = False
    _inherits = {"product.product": "product_id"}
    _inherit = [
        "website.sale.product.mixin",
        "website.searchable.mixin",
    ]

    id = fields.Char()
    event_id = fields.Many2one("event.event")
    product_id = fields.Many2one("product.product")
    combination_id = fields.Many2one("resource.booking.combination")
    # resource_ids = fields.Many2many(
    #     "resource.resource",
    #     related="combination_id.resource_ids",
    # )

    # Computed fields
    available = fields.Boolean(compute="_compute_available", search="_search_available")
    # pav_ids = fields.Many2many(
    #     "product.attribute.value",
    #     relation="resource_booking_type_product_attribute_value_rel",
    #     related="resource_booking_type_id.product_attribute_value_ids",
    # )
    # pav_tag_ids = fields.Many2many(
    #     "product.attribute.value.tag",
    #     compute="_compute_pav_tag_ids",
    # )

    # def _compute_pav_tag_ids(self):
    #     for record in self:
    #         pav_ids = record.pav_ids
    #         record.pav_tag_ids = pav_ids.tag_ids

    def _compute_available(self):
        # records_per_event = self.grouped("event_id") # 17.0
        records_per_event = defaultdict(lambda: self.env["event.booking.combination"])
        for record in self:
            records_per_event[record.event_id] |= record

        bookings = self.env["resource.booking"].search([])

        for event, records in records_per_event.items():
            filtered_bookings = bookings.filtered(
                lambda b:
                (b.start >= event.date_begin and b.start < event.date_end)
                or
                (b.stop > event.date_begin and b.stop <= event.date_end)
            )
            for record in records:
                # Available if no intersection of resources
                record.available = not bool(
                    record.combination_id.resource_ids
                    &
                    filtered_bookings.combination_id.resource_ids
                )
    
    def _search_available(self, operator, value):
        compare = {
            "=": "in",
            "!=": "not in",
        }
        assert operator in compare and value in (True, False)
        future = self.search([("event_id.date_end", ">", datetime.now())])
        filtered = future.filtered(lambda r: r.available == value)
        return [('id', compare[operator], filtered.ids)]

    def init(self):
        tools.drop_view_if_exists(self._cr, "event_booking_combination")

        pp = self.env["product.product"]
        pt = self.env["product.template"]
        ee = self.env["event.event"]
        rbt = self.env["resource.booking.type"]
        rbc = self.env["resource.booking.combination"]

        # Get all stored columns (except "id") of the first model
        # Add missing columns of the next models.
        models = [("pp", pp), ("pt", pt), ("ee", ee), ("rbt", rbt), ("rbc", rbc)]

        # col_names = {"id", "product_id"}
        # columns = ["ee.id::text || '_' || pp.id::text AS id", "pp.id AS product_id"]
        column_name_expr = [
            ("id", "ee.id::text || '_' || pp.id::text || '_' || rbc.id::text"),
            ("event_id", "ee.id"),
            ("product_id", "pp.id"),
            ("combination_id", "rbc.id"),
            # (
            #     "available",
            #     """CASE 
            #     WHEN EXISTS (
            #         SELECT 1
            #         FROM resource_booking rb
            #         JOIN resource_booking_combination_resource_resource_rel rbc_rr
            #             ON rbc_rr.resource_booking_combination_id = ebc.combination_id
            #         JOIN resource_resource rr ON rr.id = rbc_rr.resource_resource_id
            #         WHERE rb.resource_booking_combination_id = rbc_rr.resource_booking_combination_id
            #         AND (
            #             (ee.date_begin <= rb.start AND rb.start < ee.date_end)
            #             OR
            #             (ee.date_end >= rb.stop AND rb.stop > ee.date_begin)
            #         )
            #     ) THEN FALSE
            #     ELSE TRUE
            #     END""",
            # ),
        ]
        # col_names = [name for name, _ in column_name_expr]

        for code, Model in models:
            for name, field in Model._fields.items():
                if field.store and field.column_type:
                    if name not in [c[0] for c in column_name_expr]:
                        column_name_expr.append((name, code + "." + name))
                        # col_names.add(name)
                        # columns.append(code + "." + name)
        select = ["{} AS {}".format(expr, name) for name, expr in column_name_expr]

        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW event_booking_combination AS
            SELECT {", ".join(select)}
            FROM product_template_event_rel pt_ee
            JOIN event_event ee ON pt_ee.event_event_id = ee.id
            JOIN product_template pt ON pt_ee.product_template_id = pt.id
            JOIN product_product pp ON pp.product_tmpl_id = pt.id
            JOIN resource_booking_type rbt ON pp.resource_booking_type_id = rbt.id
            JOIN resource_booking_type_combination_rel rbt_rbc ON rbt_rbc.type_id = rbt.id
            JOIN resource_booking_combination rbc ON rbt_rbc.combination_id = rbc.id
            """
        )
