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
                self = self.with_context(teamm_bed_counter=i+1)
                records |= self._teamm2odoo_set_record()
        else:
            records = self._teamm2odoo_set_record()

        return records

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        counter = self.env.context.get("teamm_bed_counter")
        if counter:
            kwargs["name"] = self.env["teamm"].bed_name(counter)
        else:
            kwargs["name"] = self.env["resource.group"]._teamm2odoo_search().name
        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        kwargs = self._teamm2odoo_search_kwargs(kwargs)

        calendar = self.env.ref("event_sale_resource_booking.resource_calendar")

        group = self.env["resource.group"]._teamm2odoo_search()

        kwargs |= {
            "resource_type": "material",
            "calendar_id": calendar.id,
            "group_id": group and group.id or False,
        }

        return super()._teamm2odoo_values(kwargs)
