from collections.abc import Iterable

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _teamm2odoo(self, teamm_values):
        TeamM = self.env["teamm"]
        record = self._teamm2odoo_search(teamm_values, max_1=True)
        odoo_values = self._teamm2odoo_values(teamm_values)
        record = TeamM._create_or_write(record, odoo_values)
        return record

    @api.model
    def _teamm2odoo_search(self, teamm_values, max_1):
        domain = self._teamm2odoo_domain(teamm_values)
        records = self.search(domain)
        if max_1:
            assert len(records) in (0, 1)
        return records
    
    @api.model
    def _teamm2odoo_domain(self, teamm_values):
        domain = [("name", "in", self._teamm2odoo_names(teamm_values))]
        return domain

    @api.model
    def _teamm2odoo_values(self, teamm_values):
        return {"name": self._teamm2odoo_names(teamm_values)[0]}

    @api.model
    def _teamm2odoo_names(self, teamm_values):
        # Return list of names
        # E.g. a product template may have multiple product attributes.
        key = self._teamm2odoo_key(self._name)
        if key:
            return [name.strip() for name in teamm_values[key].split(",")]
        else:
            return []

    def _teamm2odoo_key(self, name):
        # Get a key which exists in teamm_values. Search for name and its aliases.
        names = self.env.context["teamm_aliases"].get(name, [name])
        # Get the first key found in teamm_values
        teamm_values = self.env.context["teamm_values"]
        key = next((n for n in names if n in teamm_values), None)
        return key

    def _teamm2odoo_after_create(self):
        pass
