from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

