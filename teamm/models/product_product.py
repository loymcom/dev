from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _teamm2odoo_domain(self, kwargs):
        TeamM = self.env["teamm"]

        program_name = self._teamm2odoo_get_value("program") or TeamM.DEFAULT_PROGRAM
        booking_type = TeamM.get_booking_type()
        
        # Finally
        kwargs = {
            "name": program_name,
            "resource_booking_type_id": booking_type.id,
        }
        return super()._teamm2odoo_domain(kwargs)
