from odoo import _, api, fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    @api.model
    def _teamm2odoo(self):
        records = self._teamm2odoo_set_record()

        beds = self._teamm2odoo_get_value("room size")
        if beds and int(beds) > 1:
            name = self.env["teamm"].booking_type_shared()
            records |= self._teamm2odoo_set_record({"name": name})

        return records
