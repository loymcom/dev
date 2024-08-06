import logging

from odoo import api, fields, models, tools

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
        rbs = self.env["resource.booking.session"]
        # Get all stored columns of the first model, add columns of the next models.
        models = [("pp", pp), ("pt", pt), ("rbs", rbs)]

        col_names = {"id", "product_id"}
        columns = ["rbs.id::text || '_' || pp.id::text AS id", "pp.id AS product_id"]

        for code, Model in models:
            for name, field in Model._fields.items():
                if field.store and field.column_type and name not in {"id"} | col_names:
                    col_names.add(name)
                    columns.append(code + "." + name)

        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW shop_product AS
            SELECT {", ".join(columns)}
            FROM resource_booking_session_for_product_template_rel rbs_pt
            JOIN resource_booking_session rbs ON rbs_pt.resource_booking_session_id = rbs.id
            JOIN product_template pt ON rbs_pt.product_template_id = pt.id
            JOIN product_product pp ON pp.product_tmpl_id = pt.id
            """
        )
