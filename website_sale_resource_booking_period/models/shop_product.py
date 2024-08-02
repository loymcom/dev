import pytz
from collections import defaultdict
from datetime import timedelta
import logging

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.addons.resource.models.resource import Intervals
from odoo.addons.resource_booking.models.resource_booking import _availability_is_fitting

_logger = logging.getLogger(__name__)


class ShopProduct(models.Model):
    _name = "shop.product"
    _description = "shop.product"
    _inherit = "product.product"
    _table = "product_product"
    _auto = False

    product_template_attribute_value_id = fields.Many2many(
        comodel_name="product.template.attribute.value",
        relation="product_variant_combination",
        column1="product_product_id",
        column2="product_template_attribute_value_id",
    )

    def init(self):
        tools.drop_view_if_exists(self._cr, "shop_product")

        Product = self.env["product.product"]
        column_fields = [
            field for name, field in Product._fields.items()
            if field.base_field.store and field.base_field.column_type and name != "id"
        ]
        query = Product._search([])

        context = self.env.context
        ShopProduct = self
        self = Product
        ################################################################################
        # COPIED FROM def _read(self, field_names):
        # the query may involve several tables: we need fully-qualified names
        def qualify(field):
            qname = self._inherits_join_calc(self._table, field.name, query)
            if field.type == 'binary' and (
                    context.get('bin_size') or context.get('bin_size_' + field.name)):
                # PG 9.2 introduces conflicting pg_size_pretty(numeric) -> need ::cast
                qname = f'pg_size_pretty(length({qname})::bigint)'
            return f'{qname} AS "{field.name}"'

        # selected fields are: 'id' followed by column_fields
        qual_names = [qualify(field) for field in [self._fields['id']] + column_fields]
        ################################################################################
        self = ShopProduct

        query_str, params = query.select(*qual_names)
        _logger.warning(query_str)
        _logger.warning(params)
        self._cr.execute(
            f"CREATE OR REPLACE VIEW shop_product AS {query_str}", params
        )
