from odoo import _, api, fields, models


class ResourceBookingTypeCombinationRel(models.Model):
    _inherit = "resource.booking.type.combination.rel"

    @api.model
    def _teamm2odoo_search(self, teamm_values):
        types = self.env["resource.booking.type"]._teamm2odoo_search(teamm_values)
        comb = self.env["resource.booking.combination"]._teamm2odoo_search(teamm_values)
        domain = [("type_id", "in", types.ids), ("combination_id", "in", comb.ids)]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        types = self.env["resource.booking.type"]._teamm2odoo_search(teamm_values)
        comb = self.env["resource.booking.combination"]._teamm2odoo_search(teamm_values)
        odoo_values = []
        for combination in comb:
            type_name = teamm_values["resource.booking.type"]
            if teamm_values.get("room size"):            
                if len(combination.resource_ids) < int(teamm_values.get("room size")):
                    type_name += " (shared)"
            odoo_values.append(
                {
                    "type_id": types.filtered(lambda t: t.name == type_name).id,
                    "combination_id": combination.id,
                }
            )
        return odoo_values
