import csv
import io

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError


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
            record = Model.search(Model._team_m_search(odoo_values))
            if record:
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


    # def action_import_contacts(self):
    #     Partner = self.env["res.partner"]
    #     PartnerCategory = self.env["res.partner.category"]
    #     Country = self.env["res.country"]



    #     contact_ids = []
    #     for values in csv_reader:
    #         if values["Country"] == "Norge":
    #             values["Country"] = "NO"
    #         birthdate = None
    #         if values.get('Birth date') != "! Not entered":
    #             birthdate = _mdy_date(values['Birth date'])
    #         category_names = [category.strip() for category in values["Customer Category"].split(",")]
    #         categories = PartnerCategory.search([('name', 'in', category_names)])
    #         odoo_values = {
    #             'name': values['Name'],
    #             'birthdate_date': birthdate,
    #             'ref': values['Record ID - Contact - Hubspot'],
    #             'category_id': [(6, 0, categories.ids)],
    #             'x_new_guest_year': values['New guest year'],
    #             'firstname': values['First name'],
    #             'gender': GENDER[values['Gender']],
    #             'lastname': values['Last name'],
    #             'country_id': Country.search([("code", "=", values["Country"])]).id,
    #             'city': values['City'],
    #             'zip': values['Zip'],
    #             'email': values['Email'],
    #             'street': values['Street'],
    #             'phone': values['Phone'],
    #         }
    #         contact_name = values["First name"] + " " + values["Last name"]
    #         contact = Partner.search([("name", "=", contact_name)])
    #         if contact:
    #             contact.write(odoo_values)
    #         else:
    #             contact = Partner.create(odoo_values)
    #         contact_ids.append(contact.id)





    # def action_import_products(self):
    #     pass


    # def action_import_sale_orders(self):
    #     Order = self.env["sale.order"]
    #     Contact = self.env["res.partner"]

    #     csv_file_like = io.StringIO(self.csv.strip())
    #     csv_reader = csv.DictReader(csv_file_like)

    #     for values in csv_reader:
    #         order_values = {
    #             "name": values['Ordre nr.'],
    #             "partner_id": Contact.search([('ref', "=", values['Record ID - Contact - Hubspot'])]).id,
    #             "date_order": _mdy_date(values['Booked at'])
    #         }
    #         order = Order.search([("name", "=", order_values["name"])])
    #         if not order:
    #             order = Order.create(order_values)
    #         order_line_values = {
    #             "order_id": order.id,
    #             'start_date': _mdy_date(values['From']),
    #             'end_date': _mdy_date(values['To']),
    #             "product_uom_qty": 1,
    #             "price_unit": 10000,

    #         }



    #     # "order_id": sale_order_id,
    #     #     "product_id": product_product_id,
    #     #     "start_date": "2024-05-15",
    #     #     "end_date": "2024-05-25",
    #     #     "product_uom_qty": 1, # will auto-create 1 booking if the product.product resource_booking_type_id is set.
    #     #     "price_unit": 10000,

