from datetime import datetime

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_dates(self):
        date_start = None
        date_end = None

        context = self.env.context
        date_format = self.env["res.lang"].search([("code", "=", context["lang"])]).date_format

        domain = context.get("domain") or []
        for d in domain:
            if isinstance(d, list) or isinstance(d, tuple):
                if isinstance(d[0], str) and d[0] == "date_start":
                    date_start = d[2]
                if isinstance(d[0], str) and d[0] == "date_end":
                    date_end = d[2]
        if date_start:
            date_start = datetime.strptime(date_start, date_format)
        if date_end:
            date_end = datetime.strptime(date_end, date_format)

        for record in self:
            record.date_start = date_start
            record.date_end = date_end

    def _compute_partner_id(self):
        partner_id = self.env.context.get("partner_id")
        for record in self:
            record.partner_id = partner_id

    # TODO: Prefix all of them with booking_?
    date_range_id = fields.Many2one("date.range", string="Date Range")
    date_start = fields.Date(string="Start date", compute="_compute_dates")
    date_end = fields.Date(string="End date", compute="_compute_dates")
    partner_id = fields.Many2one("res.partner", string="Contact", compute="_compute_partner_id")

    # def _compute_resource_booking(self):
    #     for record in self:
    #         tmpl = record.product_tmpl_id
    #         record.resource_booking_type_id = tmpl.resource_booking_type_id


    # From sale_resource_booking
    resource_booking_type_id = fields.Many2one(
        "resource.booking.type",
        string="Booking type",
        index=True,
        ondelete="restrict",
        help="If set, one pending booking will be generated when sold.",
        # compute="_compute_resource_booking",
    )
    resource_booking_type_combination_rel_id = fields.Many2one(
        "resource.booking.type.combination.rel",
        string="Resource combination",
        index=True,
        ondelete="restrict",
        domain="[('type_id', '=', resource_booking_type_id)]",
        help=(
            "If set, the booking will be created with this resource combination. "
            "Otherwise, the combination will be assigned automatically later, "
            "when the requester schedules the booking."
        ),
        # compute="_compute_resource_booking",
    )

    # def _do_after_create_or_write(self, create=None, write=None):
    #     super()._do_after_create_or_write(create, write)
    #     # If different types on different variants: remove from product template.
    #     if self.env.context.get("resource_booking_type_loop"):
    #         return
    #     product_templates = self.mapped("product_tmpl_id")
    #     for tmpl in product_templates:
    #         types = set(v.resource_booking_type_id for v in tmpl.product_variant_ids)
    #         combinations = set(v.resource_booking_type_combination_rel_id for v in tmpl.product_variant_ids)
    #         if len(types) > 1 or len(combinations) > 1:
    #             if tmpl.resource_booking_type_id or tmpl.resource_booking_type_combination_rel_id:
    #                 tmpl.with_context(resource_booking_type_loop=True).write(
    #                     {
    #                         "resource_booking_type_id": None,
    #                         "resource_booking_type_combination_rel_id": None,
    #                     }
    #                 )

    def create_sale_order_and_resource_booking(self):
        pass

    @api.model
    def web_search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):  # 16.0: count_limit=None
        self = self.with_context(domain=domain)
        return super().web_search_read(domain, fields, offset, limit, order)
