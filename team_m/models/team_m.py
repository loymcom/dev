import csv
import logging
import io
import json
import requests

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class TeamM(models.Model):
    _name = "team.m"

    def _mdy_date(self, mdy):
        return datetime.strptime(mdy, "%m/%d/%Y")

    name = fields.Char()
    model_ids = fields.One2many("team.m.model", "team_m_id", string="Models")
    url = fields.Char()
    param_ids = fields.One2many("team.m.param", "team_m_id", string="Params")
    csv = fields.Text()

    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"), ("done", "Done")], default="new")

    def action_import_api(self):
        self.ensure_one()
        Param = self.env["ir.config_parameter"].sudo()
        headers = {
            "X-API-SECRET-KEY": Param.get_param("X-API-SECRET-KEY"),
            "X-API-PUBLIC-KEY": Param.get_param("X-API-PUBLIC-KEY"),
            "X-API-APP-ID": Param.get_param("X-API-APP-ID"),
        }
        params = {p.key: p.value for p in self.param_ids}
        response = requests.get(self.url, headers=headers, params=params)
        if response.status_code != 200:
            raise UserError(response.text)
        return self._action_import(response.json())

    def action_import_csv(self):
        csv_file_like = io.StringIO(self.csv.strip())
        csv_reader = csv.DictReader(csv_file_like)
        return self._action_import(csv_reader)

    def _action_import(self, values_list):
        record_ids = []
        model_names = self.model_ids.filtered("is_active").mapped("name")
        for model_name in model_names:
            record_ids = []
            for values in values_list:
                Model = self.env[model_name].with_context(team_m_url=self.url)
                odoo_values = Model._team_m_to_odoo_values(values)
                record = Model._team_m_to_odoo_search(values)
                if record:
                    record.write(odoo_values)
                else:
                    record = Model.create(odoo_values)
                    Model._team_m_to_odoo_after_create(record)
                record_ids.append(record.id)

        if len(model_names) == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Imported from Team M",
                "res_model": model_names[0],
                "views": [[False, "tree"]],
                "domain": [("id", "in", record_ids)],
            }
