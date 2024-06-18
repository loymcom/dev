import csv
import io

from odoo import api, fields, models
from odoo.exceptions import UserError

GENDER = {
    "F": "female",
    "M": "male",
    "": ""
}

class TeamM(models.Model):
    _name = "team.m"

    name = fields.Char()
    csv = fields.Text()

    active = fields.Boolean(default=True)
    state = fields.Selection([("new", "New"), ("done", "Done")], default="new")

    def action_team_m(self):
        Partner = self.env["res.partner"]
        Country = self.env["res.country"]

        csv_file_like = io.StringIO(self.csv.strip())
        csv_reader = csv.DictReader(csv_file_like)

        contact_ids = []
        for values in csv_reader:
            if values["Country"] == "Norge":
                values["Country"] = "NO"
            odoo_values = {
                'name': values['Name'],
                # 'birthdate_date': values['Birth date'],
                'ref': values['Record ID - Contact - Hubspot'],
                # 'category_id': values['Customer Category'],
                # 'x_new_guest_year': values['New guest year'],
                'firstname': values['First name'],
                'gender': GENDER[values['Gender']],
                'lastname': values['Last name'],
                'country_id': Country.search([("code", "=", values["Country"])]).id,
                'city': values['City'],
                'zip': values['Zip'],
                'email': values['Email'],
                'street': values['Street'],
                'phone': values['Phone'],
            }
            contact_name = values["First name"] + " " + values["Last name"]
            contact = Partner.search([("name", "=", contact_name)])
            if contact:
                contact.write(odoo_values)
            else:
                contact = Partner.create(odoo_values)
            contact_ids.append(contact.id)


        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "views": [[False, "tree"]],
            "domain": [("id", "in", contact_ids)],
            # "target": "new",
        }

        # Iterate over the rows in the DictReader
        mylist = []
        for row in csv_reader:
            # Each row is a dictionary
            mylist.append(row)
        raise UserError(str(mylist))


