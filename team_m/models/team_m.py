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
    url = fields.Char()
    param_ids = fields.One2many("team.m.param", "team_m_id")
    model = fields.Char()
    csv = fields.Text()

    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"), ("done", "Done")], default="new")

    def action_import_works(self):
        Param = self.env["ir.config_parameter"].sudo()
        app_id = Param.get_param("X-API-APP-ID")
        public_key = Param.get_param("X-API-PUBLIC-KEY")
        secret_key = Param.get_param("X-API-SECRET-KEY")

        url = "https://dev.api.teamm.work/orders/list"
        headers = {
            "X-API-SECRET-KEY": secret_key,
            "X-API-PUBLIC-KEY": public_key,
            "X-API-APP-ID": app_id,
        }
        # raise UserError(str(headers))

        # Define the parameters
        params = {
            "startDate": "2024-01-20",
            "endDate": "2024-06-03"
        }

        # Make the GET request
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            response_list = response.json()
            raise UserError(str(response_list[0])) # each object is a dictionary. str() will return a visible result.
        else:
            raise UserError(response.text)

    def action_import(self):
        self.ensure_one()
        Model = self.env[self.model]
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

        record_ids = []
        for values in response.json():
            odoo_values = Model._team_m_to_odoo_values(values, self.url)
            _logger.warning(odoo_values)
            record = Model.search(Model._team_m_to_odoo_search(values, self.url))
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

    def action_import_csv(self):
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
