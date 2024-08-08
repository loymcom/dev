from collections.abc import Iterable

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _teamm2odoo(self):
        TeamM = self.env["teamm"]
        record = self._teamm2odoo_search(max_1=True)
        odoo_values = self._teamm2odoo_values()
        record = record._teamm2odoo_set_record(odoo_values)
        return record

    @api.model
    def _teamm2odoo_search(self, max_1):
        domain = self._teamm2odoo_domain()
        records = self.search(domain)
        if max_1:
            assert len(records) in (0, 1)
        return records
    
    @api.model
    def _teamm2odoo_domain(self):
        domain = [("name", "in", self._teamm2odoo_names())]
        return domain

    @api.model
    def _teamm2odoo_values(self):
        return {"name": self._teamm2odoo_names()[0]}

    @api.model
    def _teamm2odoo_names(self):
        # Return list of names
        # E.g. a product template may have multiple product attributes.
        names = self._teamm2odoo_get_value(self._name)
        if names:
            return names.split(",")
        else:
            return []

    def _teamm2odoo_get_value(self, key):
        # Get a key which exists in teamm_values. Search for the key and its aliases.
        try_keys = self.env.context["teamm_aliases"].get(key, [key])
        # Get the first key found in teamm_values
        teamm_values = self.env.context["teamm_values"]
        key = next((k for k in try_keys if k in teamm_values), None)
        return teamm_values.get(key)
    
    def _teamm2odoo_set_record(self, odoo_values):
        record = self
        if len(record) == 1:
            record.write(odoo_values)
        else:
            record = record.create(odoo_values)
            record._teamm2odoo_after_create()
        return record

    def _teamm2odoo_after_create(self):
        pass
