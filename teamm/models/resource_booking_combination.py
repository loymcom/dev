from odoo import _, api, fields, models


class ResourceBookingCombination(models.Model):
    _inherit = "resource.booking.combination"

    @api.model
    def _teamm2odoo(self):
        TeamM = self.env["teamm"]
        records = self
        resources = self.env["resource.resource"]

        
        beds = self._teamm2odoo_get_value("room size")
        if beds and int(beds) > 1:
            # A record for each bed
            for i in range(int(beds)):
                name = TeamM.bed_name(i + 1)
                resource = resources._teamm2odoo_search({"name": name})
                record = self._teamm2odoo_search({"resource_ids": resource.ids})
                odoo_values = self._teamm2odoo_values(resource)
                records |= record._teamm2odoo_set_record(odoo_values)
                resources |= resource
            # A record for all beds
            record = self._teamm2odoo_search({"resource_ids": resources.ids})
            odoo_values = self._teamm2odoo_values(resources)
            records |= record._teamm2odoo_set_record(odoo_values)
        else:
            # A record for the resource
            resource = resources._teamm2odoo_search({})
            record = self._teamm2odoo_search({"resource_ids": resource.ids})
            odoo_values = self._teamm2odoo_values(resource)
            records |= record._teamm2odoo_set_record(odoo_values)

        return records

    @api.model
    def _teamm2odoo_search(self, kwargs):
        domain = [("resource_ids", "in", kwargs["resource_ids"])]
        record = self.search(domain).filtered(
            lambda r: r.resource_ids.ids == kwargs["resource_ids"]
        )
        assert len(record) in (0, 1)
        return record

    @api.model
    def _teamm2odoo_values(self, resources):
        odoo_values = {"resource_ids": [fields.Command.set(resources.ids)]}
        return odoo_values
