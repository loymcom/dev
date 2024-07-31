from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _teamm2odoo_search(self, teamm_values, discount=None):
        TeamM = self.env["teamm"]
        attr_val = "product_template_variant_value_ids.product_attribute_value_id.name"

        if discount:
            domain = [(attr_val, "=", discount)]
            return self.search(domain)
        elif teamm_values.get("room sharing") in ("Private", "Share room"):
            domain = TeamM.room_booking_type_domain(teamm_values, attr_val)
            name = "NEWSTART Gold"
            _logger.warning(name)
            domain.append(
                ("name", "=", teamm_values.get("program") or TeamM.DEFAULT_PROGRAM)
                # (('name', '->>', 'en_US'), "=", name)
                # ('name', '::jsonb', '{"en_US": "NEWSTART Gold"}')
                # ("name", "ilike", name)
            )
            _logger.warning(domain)
            # _logger.warning(teamm_values.get("program"))
            # _logger.warning("ø")
            return self.search(domain)
        else:
            return super()._teamm2odoo_search(teamm_values)
