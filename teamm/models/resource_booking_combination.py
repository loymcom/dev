from odoo import _, api, fields, models


class ResourceBookingCombination(models.Model):
    _inherit = "resource.booking.combination"

    @api.model
    def _teamm2odoo(self):
        TeamM = self.env["teamm"]
        Resource = self.env["resource.resource"]

        records = self
        resources = Resource
        
        beds = self._teamm2odoo_get_value("room size")
        if beds and int(beds) > 1:
            # A record for each bed
            for i in range(int(beds)):
                resource_name = TeamM.bed_name(i + 1)
                resource = Resource._teamm2odoo_search({"name": resource_name})
                records |= self._teamm2odoo_set_record({"resource_ids": resource.ids})
                resources |= resource
            # A record for all beds
            records |= self._teamm2odoo_set_record({"resource_ids": resources.ids})
        else:
            # A record for the resource
            resource = Resource._teamm2odoo_search({})
            records |= self._teamm2odoo_set_record({"resource_ids": resource.ids})

        return records
