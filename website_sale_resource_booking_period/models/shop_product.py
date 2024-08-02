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
    _inherit = "product.product"
    _table = "product_product"
    _auto = False

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
        models = [("pp", pp), ("pt", pt)] # Get all fields of the first model

        col_names = set("id")
        columns = ["pp.id"]

        for code, Model in models:
            for name, field in Model._fields.items():
                if field.store and field.column_type and name not in {"id"} | col_names:
                    col_names.add(name)
                    columns.append(code + "." + name)

        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW shop_product AS
            SELECT {", ".join(columns)}
            FROM product_template pt
            JOIN product_product pp ON pp.product_tmpl_id = pt.id
            """
        )
