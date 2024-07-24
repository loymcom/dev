import csv
import logging
import io
import json
import requests

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

RENAME = {
    "record id - contact - hubspot": "hubspot contact",
    "ordre nr. ": "sale.order",
}

class TeamM(models.Model):
    _name = "teamm"
    _order = "sequence"

    sequence = fields.Integer()
    name = fields.Char()
    model_ids = fields.One2many("teamm.model", "teamm_id", string="Models")
    url = fields.Char()
    param_ids = fields.One2many("teamm.param", "teamm_id", string="Params")
    csv = fields.Text()
    date_format = fields.Char()

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
        return self._action_import([line for line in csv_reader])

    def _action_import(self, values_list):
        record_ids = []
        model_names = self.model_ids.filtered("is_active").mapped("name")
        for model_name in model_names:
            record_ids = []
            for values in values_list:
                values = {
                    RENAME.get(key.lower(), key.lower()): value
                    for key, value in values.items()
                }
                Model = self.env[model_name].with_context(
                    teamm_url=self.url,
                    teamm_date_format=self.date_format,
                )
                odoo_values = Model._teamm2odoo_values(values)
                records = Model._teamm2odoo_search(values)
                if records:
                    if type(odoo_values) is dict:
                        records.write(odoo_values)
                else:
                    record = Model.create(odoo_values)
                    Model._teamm2odoo_after_create(record)
                    records = record
                record_ids.extend(records.ids)

        if len(model_names) == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Imported from Team M",
                "res_model": model_names[0],
                "views": [[False, "tree"]],
                "domain": [("id", "in", record_ids)],
            }

    #
    # Used by other models
    #
    
    def _get_date(self, datestring):
        return datetime.strptime(datestring, self.env.context["teamm_date_format"])

    # res.partner
    GENDER = {
        "F": "female",
        "M": "male",
        "": ""
    }

    # product.product
    ROOM = {
        "1": "Single",
        "2": "Double",
    }

    # resource.resource
    def room_name(self, teamm_values):
        return "Room {standard} {number}".format(
            standard=teamm_values["resource.booking.type"].split()[0],
            number=teamm_values["resource.resource"],
        )
