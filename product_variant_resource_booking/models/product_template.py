from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends("product_variant_ids.resource_booking_type_id", "product_variant_ids.resource_booking_type_combination_rel_id")
    def _compute_resource_booking_type(self):
        for tmpl in self:
            type = set(v.resource_booking_type_id.id for v in tmpl.product_variant_ids)
            combination = set(v.resource_booking_type_combination_rel_id.id for v in tmpl.product_variant_ids)
            _logger.warning(type)
            _logger.warning(combination)
            tmpl.resource_booking_type_id = type.pop() if len(type) == 1 else None
            tmpl.resource_booking_type_combination_rel_id = combination.pop() if len(combination) == 1 else None

    def _inverse_resource_booking_type(self):
        for tmpl in self:
            variants = tmpl.product_variant_ids
            variants.resource_booking_type_id = tmpl.resource_booking_type_id
            variants.resource_booking_type_combination_rel_id = tmpl.resource_booking_type_combination_rel_id

    # @api.depends("product_variant_ids.resource_booking_type_id")
    # def _compute_resource_booking_hide(self):

    resource_booking_type_id = fields.Many2one(
        compute="_compute_resource_booking_type",
        inverse="_inverse_resource_booking_type",
        store=False,
    )
    resource_booking_type_combination_rel_id = fields.Many2one(
        compute="_compute_resource_booking_type",
        inverse="_inverse_resource_booking_type",
        store=False,
    )
    resource_booking_hide = fields.Boolean(compute="_compute_resource_booking_hide")

    # def _do_after_create_or_write(self, create=None, write=None):
    #     super()._do_after_create_or_write(create, write)
    #     # Update variants
    #     if self.env.context.get("resource_booking_type_loop"):
    #         return
    #     product_vals = {}
    #     if "resource_booking_type_id" in vals:
    #         product_vals["resource_booking_type_id"] = vals["resource_booking_type_id"]
    #     if "resource_booking_type_combination_rel_id" in vals:
    #         product_vals["resource_booking_type_combination_rel_id"] = vals["resource_booking_type_combination_rel_id"]
    #     if product_vals:
    #         products = self.env["product.product"].search([("​product_template_attribute_value_ids.product_attribute_value_id", "in", self.ids)])
    #         products.write(product_vals)

    #     product_templates = self.mapped("product_tmpl_id")
    #     for tmpl in product_templates:
    #         types = set(v.resource_booking_type_id for v in tmpl.product_variant_ids)
    #         combinations = set(v.resource_booking_type_combination_rel_id for v in tmpl.product_variant_ids)
    #         if len(types) > 1 or len(combinations) > 1:
    #             tmpl.with_context(resource_booking_type=True).write(
    #                 {
    #                     "resource_booking_type_id": None,
    #                     "resource_booking_type_combination_rel_id": None,
    #                 }
    #             )

    date_range_ids = fields.Many2many(
        comodel_name="date.range",
        relation="product_template_date_range_rel",
        string="Date Ranges",
    )
