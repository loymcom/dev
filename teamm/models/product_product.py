from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        TeamM = self.env["teamm"]

        discount = self.env.context.get("teamm_discount")
        if discount:
            if discount.name.lower().startswith("gavekort"):
                debug = True
            pav = self.env["product.attribute.value"]._teamm2odoo_search()
            ptav = self.env["product.template.attribute.value"].search(
                [("product_attribute_value_id", "=", pav.id)]
            )
            kwargs |= {
                "name": TeamM.DISCOUNT,
                "product_template_attribute_value_ids": ptav.ids,
            }
        else:
            program_name = self._teamm2odoo_get_value("program") or TeamM.DEFAULT_PROGRAM
            booking_type = self.env["resource.booking.type"]._teamm2odoo_search()
            kwargs |= {
                "name": program_name,
                "resource_booking_type_id": booking_type.id,
            }
        return super()._teamm2odoo_search_kwargs(kwargs)
