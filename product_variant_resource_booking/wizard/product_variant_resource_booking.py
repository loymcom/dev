from odoo import api, fields, models


class ProductVariantResourceBooking(models.TransientModel):
    _name = "product.variant.resource.booking"
    _description = "Product Variant Resource Booking Wizard"

    def _compute_name(self):
        date_format = self.env["res.lang"].search([("code", "=", self.env.context["lang"])]).date_format
        for record in self:
            record.name = "{} {}-{} ({})".format(
                record.partner_id.name if record.partner_id else "",
                record.date_start.strftime(date_format) if record.date_start else "",
                record.date_end.strftime(date_format) if record.date_end else "",
                record.date_range_id.name if record.date_range_id else "",
            )

    name = fields.Char(compute="_compute_name")
    date_range_id = fields.Many2one("date.range", string="Date Range")
    date_start = fields.Date(string="Start date")
    date_end = fields.Date(string="End date")
    partner_id = fields.Many2one("res.partner", string="Contact")
    product_attribute_value_id = fields.Many2one(
        "product.attribute.value",
        string="Resource Type",
        domain=lambda self: "[('id', 'in', {})]".format(self._get_resource_attr_values().ids),
    )

    @api.onchange("date_range_id")
    def _onchange_date_range_id(self):
        for record in self:
            record.date_start = record.date_range_id.date_start
            record.date_end = record.date_range_id.date_end

    def _get_resource_attr_values(self):
        resources = self.env["resource.resource"].search([])
        return resources.mapped("product_attribute_value_id")

    def view_product_product(self):
        self.ensure_one()
        date_format = self.env["res.lang"].search([("code", "=", self.env.context["lang"])]).date_format
        domain = []
        context = {}

        # Context is the easiest way to pass parameters.
        if self.partner_id:
            context["partner_id"] = self.partner_id.id

        # Domain parsing is already made for compute date_start & date_end.
        # Therefore domain is used here instead of context.
        if self.date_start and self.date_end:
            domain.extend([
                ("date_start", ">=", self.date_start.strftime(date_format)),
                ("date_end", "<=", self.date_end.strftime(date_format)),
            ])

        # Domain: Show only products connected with resources (they have the same attribute value).
        search_attr_values = self._get_resource_attr_values()

        if self.product_attribute_value_id:
            # Of the search_attr_values, keep only the selected attribute value (intersection).
            search_attr_values = search_attr_values & self.product_attribute_value_id
            ids = self.env["product.template.attribute.value"].search(
                [("product_attribute_value_id", "=", self.product_attribute_value_id.id)]
            ).ids

        template_attr_value_ids = self.env["product.template.attribute.value"].search(
            [("product_attribute_value_id", "in", search_attr_values.ids)]
        ).ids
        domain.append(("product_template_attribute_value_ids", "in", template_attr_value_ids))

        return {
            "type": "ir.actions.act_window",
            "name": "Packages",
            "res_model": "product.product",
            "views": [
                [self.env.ref("product_variant_resource_booking.product_product_view_tree").id, "tree"],
                [False, "form"],
            ],
            # "search_view_id": [self.env.ref("product_variant_resource_booking.product_product_view_search").id, "search"],
            "domain": domain,
            "context": context,
        }
