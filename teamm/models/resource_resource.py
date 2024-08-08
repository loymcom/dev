from odoo import _, api, fields, models


class ResourceResource(models.Model):
    _inherit = "resource.resource"

    @api.model
    def _teamm2odoo(self, teamm_values):
        TeamM = self.env["teamm"]
        records = self

        # A record for each bed
        beds = teamm_values.get("room size")
        if beds and int(beds) > 1:
            for i in range(int(beds)):
                name = TeamM.bed_name(teamm_values, i + 1)
                record = self._teamm2odoo_search(teamm_values, max_1=True)
                odoo_values = self._teamm2odoo_values(teamm_values, name)
                records |= TeamM._create_or_write(record, odoo_values)
        else:
            records = super()._teamm2odoo(teamm_values)

        return records

    @api.model
    def _teamm2odoo_values(self, teamm_values, name=None):
        if not name:
            name = self._teamm2odoo_names(teamm_values)[0]

        calendar = self.env["resource.calendar"]._teamm2odoo_search(teamm_values, True)
        if not len(calendar) == 1:
            calendar = self.env.ref("event_sale_resource_booking.resource_calendar")

        group = self.env["resource.group"]._teamm2odoo_search(teamm_values, max_1=True)

        odoo_values = {
            "name": name,
            "resource_type": "material",
            "calendar_id": calendar.id,
            "group_id": group and group.id or False,
        }

        return odoo_values
