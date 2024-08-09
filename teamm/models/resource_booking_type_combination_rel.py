from odoo import _, api, fields, models


class ResourceBookingTypeCombinationRel(models.Model):
    _inherit = "resource.booking.type.combination.rel"

    @api.model
    def _teamm2odoo(self):
        TeamM = self.env["teamm"]
        Resource = self.env["resource.resource"]
        Combination = self.env["resource.booking.combination"]
        Type = self.env["resource.booking.type"]

        records = self
        resources = Resource

        beds = self._teamm2odoo_get_value("room size")
        if beds and int(beds) > 1:
            # A record for each bed
            for i in range(int(beds)):
                resource_name = TeamM.bed_name(i + 1)
                resource = Resource._teamm2odoo_search({"name": resource_name})
                comb = Combination._teamm2odoo_search({"resource_ids": resource.ids})
                type_name = TeamM.booking_type_shared()
                type = Type._teamm2odoo_search({"name": type_name})
                records |= self._teamm2odoo_set_record(
                    {"type_id": type.id, "combination_id": comb.id}
                )
                resources |= resource
            # A record for all beds
            comb = Combination._teamm2odoo_search({"resource_ids": resources.ids})
            records |= self._teamm2odoo_set_record(
                {"type_id": type.id, "combination_id": comb.id}
            )
        else:
            # A record for the resource
            resource = Resource._teamm2odoo_search()
            comb = Combination._teamm2odoo_search({"resource_ids": resource.ids})
            type = Type._teamm2odoo_search()
            records |= self._teamm2odoo_set_record(
                {"type_id": type.id, "combination_id": comb.id}
            )
        return records


    # @api.model
    # def _teamm2odoo_search(self, teamm_values):
    #     types = self.env["resource.booking.type"]._teamm2odoo_search(teamm_values)
    #     comb = self.env["resource.booking.combination"]._teamm2odoo_search(teamm_values)
    #     domain = [("type_id", "in", types.ids), ("combination_id", "in", comb.ids)]
    #     return self.search(domain)

    # @api.model
    # def _teamm2odoo_values(self, teamm_values):
    #     types = self.env["resource.booking.type"]._teamm2odoo_search(teamm_values)
    #     comb = self.env["resource.booking.combination"]._teamm2odoo_search(teamm_values)
    #     odoo_values = []
    #     for combination in comb:
    #         type_name = teamm_values["resource.category"]
    #         if teamm_values.get("room size"):            
    #             if len(combination.resource_ids) < int(teamm_values["room size"]):
    #                 type_name += self.env["teamm"].SHARED_ROOM
    #         odoo_values.append(
    #             {
    #                 "type_id": types.filtered(lambda t: t.name == type_name).id,
    #                 "combination_id": combination.id,
    #             }
    #         )
    #     return odoo_values
