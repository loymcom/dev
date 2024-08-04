import logging

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)


class WebsiteEventSaleResourceBooking(models.Model):
    _name = "website.event.sale.resource.booking"
    _description = "website.event.sale.resource.booking"
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
        ee = self.env["event.event"]

        # Get all stored columns (except "id") of the first model
        # Add columns of the next models.
        models = [("pp", pp), ("pt", pt), ("ee", ee)]

        col_names = {"id", "product_id"}
        columns = ["ee.id::text || '_' || pp.id::text AS id", "pp.id AS product_id"]

        for code, Model in models:
            for name, field in Model._fields.items():
                if field.store and field.column_type and name not in {"id"} | col_names:
                    col_names.add(name)
                    columns.append(code + "." + name)

        self._cr.execute(
            f"""
            CREATE OR REPLACE VIEW website_event_sale_resource_booking AS
            SELECT {", ".join(columns)}
            FROM product_template_event_rel pt_ee
            JOIN event_event ee ON pt_ee.event_event_id = ee.id
            JOIN product_template pt ON pt_ee.product_template_id = pt.id
            JOIN product_product pp ON pp.product_tmpl_id = pt.id
            """
        )
