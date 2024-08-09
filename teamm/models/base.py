from collections.abc import Iterable

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _teamm2odoo(self):
        record = self._teamm2odoo_set_record()
        return record
    
    def _teamm2odoo_set_record(self, kwargs={}):
        record = self._teamm2odoo_search(kwargs)
        odoo_values = self._teamm2odoo_values(kwargs)
        if len(record) == 1:
            record.write(odoo_values)
        else:
            record = record.create(odoo_values)
            record._teamm2odoo_after_create()
        return record

    @api.model
    def _teamm2odoo_search(self, kwargs={}):
        domain = self._teamm2odoo_domain(kwargs)
        # Don't search if there is no search domain
        record = self.search(domain) if domain else self
        x2many = self._teamm2odoo_x2many(kwargs)
        if x2many:
            # Check if record.x2many_field.ids == kwargs[x2many_field]
            record = record.filtered(
                lambda r: all(
                    set(getattr(r, field).ids) == set(ids)
                    for field, ids in x2many.items()
                )
            )
        assert len(record) in (0, 1)
        return record
    
    @api.model
    def _teamm2odoo_domain(self, kwargs={}):
        kwargs = kwargs or self._teamm2odoo_default_kwargs()
        domain = []
        x2many = self._teamm2odoo_x2many(kwargs)
        for key, value in kwargs.items():
            operator = "in" if key in x2many else "="
            domain.append((key, operator, value))
        return domain
    
    @api.model
    def _teamm2odoo_x2many(self, kwargs):
        x2many_kwargs = {
            key: val for key, val in kwargs.items()
            if self._fields[key].type in ("one2many", "many2many")
        }
        return x2many_kwargs

    @api.model
    def _teamm2odoo_values(self, kwargs={}):
        values = kwargs or self._teamm2odoo_default_kwargs()
        for x2many_field, ids in self._teamm2odoo_x2many(values).items():
            values[x2many_field] = [fields.Command.set(ids)]
        return values
    
    @api.model
    def _teamm2odoo_default_kwargs(self):
        names = self._teamm2odoo_names()
        return {"name": names[0]} if names else {}

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

    def _teamm2odoo_after_create(self):
        pass
