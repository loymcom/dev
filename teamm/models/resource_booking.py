from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    @api.model
    def _teamm2odoo_search_kwargs(self, kwargs):
        TeamM = self.env ["teamm"]

        create_event = bool(self.env.context["teamm"].model_ids.filtered(lambda m: m.name == "event.event"))
        if create_event:
            # Identify a resource booking representing the event in timeline
            partner = self.env["res.partner"]._teamm2odoo_search()
            booking_type = self.env["resource.booking.type"]._teamm2odoo_search()
            start = TeamM._get_datetime("from")
            stop = TeamM._get_datetime("to")
            if not len(partner):
                partner = self.env.ref("base.main_partner")
            if not len(booking_type):
                booking_type = self.env.ref(
                    "event_sale_resource_booking_timeline.resource_booking_type_event"
                )
            kwargs |= {
                "partner_ids": partner.ids,
                "type_id": booking_type.id,
                "start": start,
                "duration": (stop - start).total_seconds() / 3600,
            }
        else:
            # # Assert "Private" or "Share room"
            # room_sharing = self._teamm2odoo_get_value("room sharing")
            # assert room_sharing in ("Private", "Share room")
            hubspot_deal_id = self._teamm2odoo_get_value("hubspot deal id")
            kwargs |= {
                "hubspot_deal_id": hubspot_deal_id,
            }
        # Identify a resource_booking

        return super()._teamm2odoo_search_kwargs(kwargs)

    @api.model
    def _teamm2odoo_values(self, kwargs):
        TeamM = self.env ["teamm"]
        create_event = bool(self.env.context["teamm"].model_ids.filtered(lambda m: m.name == "event.event"))
        if create_event:
            kwargs |= {
                "name": self.env["event.event"]._teamm2odoo_name(),
                "combination_auto_assign": 1,
            }
        else:
            partner = self.env["res.partner"]._teamm2odoo_search()
            product = self.env["product.product"]._teamm2odoo_search()
            combination = self._teamm2odoo_get_available_booking_combination()
            booking_type = self.env["resource.booking.type"]._teamm2odoo_search()
            start = TeamM._get_datetime("from")
            stop = TeamM._get_datetime("to")
            if not len(partner) or not len(product) or not len(combination) or not len(booking_type):
                raise ValidationError(f"Missing info:\nContact: {partner}\nProduct: {product}\nCombination: {combination}\nBooking Type: {booking_type}")

            kwargs |= {
                "name": partner.name,
                "combination_auto_assign": 0,
                "combination_id": combination.id,
                "product_id": product.id,
                "partner_ids": partner.ids,
                "type_id": booking_type.id,
                "start": start,
                "duration": (stop - start).total_seconds() / 3600,
            }
        return super()._teamm2odoo_values(kwargs)

    def _teamm2odoo_get_available_booking_combination(self):
        """ Get a booking combination for the booking. """
        room = self.env["resource.group"]._teamm2odoo_search()
        combinations = self.env["resource.booking.combination"].search(
            [("resource_ids", "in", room.resource_ids.ids)]
        )
        room_size = len(room.resource_ids)
        if room_size > 1:
            room_sharing = self._teamm2odoo_get_value("room sharing")
            if room_sharing == "Share room":
                combinations = combinations.filtered(lambda c: len(c.resource_ids) == 1)
                start = self.env["teamm"]._get_datetime("from")
                stop = self.env["teamm"]._get_datetime("to")
                this_booking = self._teamm2odoo_search()
                bookings = self.env["resource.booking"].search(
                    [
                        ("id", "!=", this_booking.id),
                        ("combination_id", "in", combinations.ids),
                        "|",
                        "&", ("start", ">=", start), ("start", "<", stop),
                        "&", ("stop", ">", start), ("stop", "<=", stop),
                    ]
                )
                available_combinations = combinations.filtered(
                    lambda c: c.id not in bookings.combination_id.ids
                )
                combination = available_combinations.sorted(key=lambda c: c.name)
                try:
                    combination = combination[0]
                except:
                    raise UserError(f"No available combinations for room {room.name} from {start} to {stop}.")
            else:
                combination = combinations.filtered(lambda c: len(c.resource_ids) > 1)
        else:
            combination = combinations
            if len(combinations) != 1:
                debug = True
        assert len(combination) == 1, f"{str(combinations)} - probably missing room size or room sharing."
        return combination
