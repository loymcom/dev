from odoo import _, api, fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        TeamM = self.env["teamm"]
        room_sharing = teamm_values.get("room sharing")
        room_size = teamm_values.get("room size")
        room_standard = teamm_values.get("room standard")
        if room_sharing and room_size and room_standard:
            share_operator, share_value = TeamM.room_sharing(teamm_values)
            domain = [
                ("name", "ilike", room_standard),
                ("name", "ilike", TeamM.ROOM[room_size]),
                ("name", share_operator, share_value)
            ]
            return self.search(domain)
        # elif teamm_values.get("resource.booking.type"):
        #     domain = [("name", "=like", teamm_values["resource.booking.type"] + "%")]
        #     return self.search(domain)
        else:
            return super()._teamm2odoo_search(teamm_values)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Calendar = self.env["resource.calendar"]
        odoo_values = {
            "name": teamm_values["resource.booking.type"],
            "duration": 240,
            "slot_duration": 24,
            "resource_calendar_id": Calendar._teamm2odoo_search(teamm_values).id,
            "period_type": teamm_values["period_type"],
        }
        if teamm_values["room size"] == "2":
            odoo_values = [
                odoo_values,
                odoo_values | {"name": odoo_values["name"] + " (shared)"},
            ]
        return odoo_values
