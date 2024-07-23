from odoo import _, api, fields, models

class ResourceBookingCombination(models.Model):
    _inherit = "resource.booking.combination"

    @api.model
    def _teamm2odoo_search(self, team_m_values):
        values = team_m_values
        resources = self.env["resource.resource"]._teamm2odoo_search(values)
        domain = [("resource_ids", "in", resources.ids)]
        return self.search(domain)

    @api.model
    def _teamm2odoo_values(self, team_m_values):
        values = team_m_values
        odoo_values = []
        resources = self.env["resource.resource"]._teamm2odoo_search(values)
        for resource in resources:
            odoo_values.append(
                {
                    "resource_ids": [fields.Command.link(resource.id)],
                }
            )
        if len(resources) == 2:
            odoo_values.append(
                {
                    "resource_ids": [fields.Command.set(resources.ids)],
                }
            )
        return odoo_values
