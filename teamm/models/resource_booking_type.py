from odoo import _, api, fields, models


class ResourceBookingType(models.Model):
    _inherit = "resource.booking.type"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        TeamM = self.env["teamm"]
        if teamm_values.get("room sharing") in ("Private", "Share room"):
            domain = TeamM.room_booking_type_domain(teamm_values, "name")
            return self.search(domain)
        elif teamm_values.get("resource.category"):
            domain = [("name", "=like", teamm_values["resource.category"] + "%")]
            return self.search(domain)
        else:
            return super()._teamm2odoo_search(teamm_values)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        Calendar = self.env["resource.calendar"]
        odoo_values = {
            "name": teamm_values.get("resource.category") or teamm_values["resource.booking.type"],
            "duration": 240,
            "slot_duration": 24,
            "resource_calendar_id": Calendar._teamm2odoo_search(teamm_values).id,
            "period_type": teamm_values["period_type"],
        }
        beds = teamm_values.get("room size")
        if beds and int(beds) > 1:
            odoo_values = [
                # first record
                odoo_values,
                # second record
                odoo_values | {
                    "name": odoo_values["name"] + self.env["teamm"].SHARED_ROOM
                },
            ]
        return odoo_values
