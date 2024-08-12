import base64
import csv
import logging
import io
import requests
import pytz

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# TODO: replace KEY & VALUE with teamm.alias
KEY = {
    "Record ID - Contact - Hubspot": "hubspot contact id",
    "Ordre nr. ": "sale.order",
}
VALUE = {
    "NEWSTART Smal": "NEWSTART Sølv",
    "Unlocx Pain Relife": "Unlocx Pain Relief",
    "Stressmestrings seminar": "Stressmestring",
    "! Not entered": "",
}

class TeamM(models.Model):
    _name = "teamm"
    _order = "sequence"

    sequence = fields.Integer()
    name = fields.Char()
    src = fields.Selection(
        [
            ('api', 'API'),
            ('csv_file', 'CSV File'),
            ('csv_field', 'CSV Field'),
        ],
        string="Data Source",
    )
    src_begin = fields.Integer(string="Begin With")
    src_end = fields.Integer(string="End With")
    model_ids = fields.One2many(
        "teamm.model",
        "teamm_id",
        string="Models",
        help="Active models will be imported. Import one at a time to see the result."
        "Primary Key and Values are only for documentation."
    )
    alias_ids = fields.One2many("teamm.alias", "teamm_id", string="Aliases")
    url = fields.Char()
    param_ids = fields.One2many("teamm.param", "teamm_id", string="Params")
    csv_file = fields.Binary(string='CSV File')
    csv_file_name = fields.Char(string='CSV Filename')
    csv = fields.Text()
    csv_delimiter = fields.Char(default=",")
    date_format = fields.Char()

    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"), ("done", "Done")], default="new")

    def action_import(self):
        method_name = "action_import_" + self.src
        method = getattr(self, method_name, None)
        return method()

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

    def action_import_csv_file(self):
        if self.csv_file:
            file_data = base64.b64decode(self.csv_file)
            csv_file = io.StringIO(file_data.decode('utf-8'))
            csv_reader = csv.DictReader(csv_file, delimiter=self.csv_delimiter)
            return self._action_import([line for line in csv_reader])
        
    def action_import_csv_field(self):
        csv_file = io.StringIO(self.csv.strip())
        csv_reader = csv.DictReader(csv_file, delimiter=self.csv_delimiter)
        return self._action_import([line for line in csv_reader])
    
    def action_clear_csv(self):
        self.csv = ""

    def _action_import(self, teamm_values_list):
        record_ids = []
        begin, end = self.src_begin, self.src_end
        model_names = self.model_ids.filtered("is_active").mapped("name")
        teamm_aliases = {
            alias.name: [alias.name] + alias.aliases.split(",")
            for alias in self.alias_ids
        }
        for model_name in model_names:
            record_ids = []
            for i, teamm_values in enumerate(teamm_values_list, start=1):
                if (begin and begin > i) or (end and end < i):
                    continue
                # Keys: rename KEY-words, strip first/last spaces, lowercase
                # Values: rename VALUE-words, strip first/last spaces
                teamm_values = {
                    # Mismatch between CSV header and rows may cause error here
                    KEY.get(key, key).strip().lower(): VALUE.get(val, val).strip()
                    for key, val in teamm_values.items()
                }
                Model = self.env[model_name].with_context(
                    teamm=self,
                    teamm_aliases=teamm_aliases,
                    teamm_values=teamm_values,
                )
                records = Model._teamm2odoo()
                record_ids.extend(records.ids)

        if len(model_names) == 1:
            return {
                "type": "ir.actions.act_window",
                "name": "Imported from Team M",
                "res_model": model_names[0],
                "views": [[False, "tree"], [False, "form"]],
                "domain": [("id", "in", record_ids)],
            }

    #
    # Used by other models
    #
    
    def _get_date(self, key):
        datestring = self._teamm2odoo_get_value(key)
        if datestring:
            return datetime.strptime(datestring, self.env.context["teamm"].date_format)
    
    def _get_datetime(self, key):
        date_string = self._teamm2odoo_get_value(key)
        date_format = self.env.context["teamm"].date_format
        naive_date = datetime.strptime(date_string, date_format)
        naive_date = naive_date.replace(hour=0, minute=0, second=0, microsecond=0)
        user_timezone = pytz.timezone(self.env.user.tz)
        local_date = user_timezone.localize(naive_date)
        utc_date = local_date.astimezone(pytz.utc)
        naive_date = utc_date.replace(tzinfo=None)
        return naive_date

    # res.partner
    GENDER = {
        "F": "female",
        "M": "male",
    }

    # product.product
    DEFAULT_PROGRAM = "No program"
    # resource.booking.type(.combination.rel)
    SHARED_ROOM = " (shared)"

    # Used for discount product and discount attribute
    DISCOUNT = "Discount"

    # # product.product (for product.attribute.value)
    # # resoure.booking.type
    # def room_booking_type_domain(self, teamm_values, field):
    #     rooms = self.env["resource.resource"]._teamm2odoo_search(teamm_values)
    #     name = rooms.category_id.name
    #     beds = int(teamm_values["room size"])
    #     if beds > 2 or (beds == 2 and teamm_values["room sharing"] == "Share room"):
    #         name += self.SHARED_ROOM
    #     return [(field, "=", name)]
    
    def booking_type_shared(self):
        BookingType = self.env["resource.booking.type"]
        name = BookingType._teamm2odoo_name() + self.SHARED_ROOM
        return name

    # resource.resource
    def bed_name(self, num):
        # return "Room {standard} {number}".format(
        #     standard=teamm_values["resource.booking.type"].split()[0],
        #     number=teamm_values["resource.resource"],
        # )

        # Booking has "room" (number) and master data has "resource.resource"
        # TODO: Include "room name" when this becomes available?
        # name = self._teamm2odoo_get(teamm_values, "room")
        teamm_values = self.env.context["teamm_values"]
        name = (
            teamm_values.get("room") or 
            teamm_values.get("resource.group") or
            teamm_values.get("resource.resource")
        )
        assert name
        name = "{name} {letter}".format(name=name, letter=chr(num + 64))
        return name
