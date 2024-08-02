import pytz
from collections import defaultdict
from datetime import timedelta
import logging

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.tools import Query
from odoo.addons.resource.models.resource import Intervals
from odoo.addons.resource_booking.models.resource_booking import _availability_is_fitting

_logger = logging.getLogger(__name__)


class ShopProduct(models.Model):
    _name = "shop.product"
    _description = "shop.product"
    _auto = False
    _inherits = {"product.product": "product_id"}
    _inherit = [
        "website.sale.product.mixin",
        "website.searchable.mixin",
    ]

    product_id = fields.Many2one("product.product")

    # product_template_attribute_value_id = fields.Many2many(
    #     comodel_name="product.template.attribute.value",
    #     relation="product_variant_combination",
    #     column2="product_product_id",
    #     column1="product_template_attribute_value_id",
    # )

    def init(self):
        tools.drop_view_if_exists(self._cr, "shop_product")

        pp = self.env["product.product"]
        pt = self.env["product.template"]
        rbp = self.env["resource.booking"] # period
        # Get all stored columns of the first model, add columns of the next models.
        models = [("pp", pp), ("pt", pt), ("rbp", rbp)]

        col_names = {"id", "product_id"}
        columns = ["rbp.id::text || '_' || pp.id::text AS id", "pp.id AS product_id"]

        for code, Model in models:
            for name, field in Model._fields.items():
                if field.store and field.column_type and name not in {"id"} | col_names:
                    col_names.add(name)
                    columns.append(code + "." + name)

        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW shop_product AS
            SELECT {", ".join(columns)}
            FROM resource_booking_period_for_product_template_rel rbp_pt
            JOIN resource_booking rbp ON rbp_pt.resource_booking_id = rbp.id
            JOIN product_template pt ON rbp_pt.product_template_id = pt.id
            JOIN product_product pp ON pp.product_tmpl_id = pt.id
            """
        )
