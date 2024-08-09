from odoo import _, api, fields, models


class ResourceResource(models.Model):
    _inherit = "resource.resource"

    @api.model
    def _teamm2odoo(self):
        TeamM = self.env["teamm"]
        records = self

        # A record for each bed
        beds = self._teamm2odoo_get_value("room size")
        if beds and int(beds) > 1:
            for i in range(int(beds)):
                name = TeamM.bed_name(i + 1)
                records |= self._teamm2odoo_set_record({"name": name})
        else:
            records = super()._teamm2odoo_set_record()

        return records

    @api.model
    def _teamm2odoo_values(self, kwargs):
        odoo_values = super()._teamm2odoo_values(kwargs)

        calendar = self.env["resource.calendar"]._teamm2odoo_search()
        if not len(calendar) == 1:
            calendar = self.env.ref("event_sale_resource_booking.resource_calendar")

        group = self.env["resource.group"]._teamm2odoo_search()

        odoo_values |= {
            "resource_type": "material",
            "calendar_id": calendar.id,
            "group_id": group and group.id or False,
        }

        return odoo_values
