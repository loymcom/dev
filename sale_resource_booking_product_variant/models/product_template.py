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

    # @api.depends("product_variant_ids.resource_booking_type_id")
    # def _compute_resource_booking_hide(self):
    resource_booking_hide = fields.Boolean(compute="_compute_resource_booking_hide")
