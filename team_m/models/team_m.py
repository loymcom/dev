import csv
import io

from odoo import api, fields, models
from odoo.exceptions import UserError


class TeamM(models.Model):
    _name = "team.m"

    name = fields.Char()
    csv = fields.Text()

    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"), ("done", "Done")], default="new")

    def action_team_m(self):
        csv_file_like = io.StringIO(self.csv.strip())
        csv_reader = csv.DictReader(csv_file_like)

        Partner = self.env["res.partner"]
        contact = None
        for values in csv_reader:
            contact_name = values["firstname"] + " " + values["lastname"]
            contact = Partner.search([("name", "=", contact_name)])
            # .write(values)
            # .unlink()
            if not contact:
                contact = Partner.create(values)

        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "views": [[False, "form"]],
            "res_id": contact[0].id,
            "target": "new",
        }

        # Iterate over the rows in the DictReader
        mylist = []
        for row in csv_reader:
            # Each row is a dictionary
            mylist.append(row)
        raise UserError(str(mylist))

