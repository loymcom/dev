import csv
import logging
import io

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class TeamM(models.Model):
    _name = "team.m"

    def _mdy_date(self, mdy):
        return datetime.strptime(mdy, "%m/%d/%Y")

    name = fields.Char()
    model = fields.Char()
    csv = fields.Text()

    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"), ("done", "Done")], default="new")

    def action_import(self):
        Model = self.env[self.model]
        csv_file_like = io.StringIO(self.csv.strip())
        csv_reader = csv.DictReader(csv_file_like)
        record_ids = []
        for values in csv_reader:
            odoo_values = Model._team_m_to_odoo(values)
            _logger.warning(odoo_values)
            record = Model.search(Model._team_m_search(values))
            if record:
                _logger.warning(record)
                record.write(odoo_values)
            else:
                record = Model.create(odoo_values)
            record_ids.append(record.id)

        return {
            "type": "ir.actions.act_window",
            "name": "Imported from Team M",
            "res_model": self.model,
            "views": [[False, "tree"]],
            "domain": [("id", "in", record_ids)],
        }
