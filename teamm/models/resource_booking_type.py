from odoo import _, api, fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    @api.model
    def _teamm2odoo(self):
        records = self._teamm2odoo_set_record()

        beds = self._teamm2odoo_get_value("room size")
        if beds and int(beds) > 1:
            name = self.env["teamm"].booking_type_shared()
            self = self.with_context(**{"resource.booking.type": name})
            records |= self._teamm2odoo_set_record()

        return records

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        TeamM = self.env["teamm"]
        create_event = bool(self.env.context["teamm"].model_ids.filtered(lambda m: m.name == "event.event"))
        create_resource = bool(self.env.context["teamm"].model_ids.filtered(lambda m: m.name == "resource.resource"))
        if create_event:
            kwargs["id"] = self.env.ref(
                "event_sale_resource_booking_timeline.resource_booking_type_event"
            ).id
        elif create_resource:
            bed_counter = self.env.context.get("teamm_bed_counter", 0)
            room_sharing = self.env.context.get("teamm_room_sharing")
            if bed_counter > 0 and room_sharing == "Share room":
                kwargs["name"] = self.env["teamm"].booking_type_shared()
        else:
            resource_group = self.env["resource.group"]._teamm2odoo_search()
            type = resource_group.resource_ids.combination_ids.type_rel_ids.type_id
            room_size = self._teamm2odoo_get_value("room size")
            if room_size and int(room_size) > 1:
                room_sharing = self._teamm2odoo_get_value("Room sharing")
                if room_sharing == "Share room":
                    type = type.filtered(lambda t: TeamM.SHARED_ROOM in t.name)
                else:
                    type = type.filtered(lambda t: TeamM.SHARED_ROOM not in t.name)
                kwargs["id"] = type.id
            else:
                kwargs["id"] = type.id

        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        calendar = self.env.ref("event_sale_resource_booking.resource_calendar")
        kwargs["resource_calendar_id"] = calendar.id
        return super()._teamm2odoo_values(kwargs)
