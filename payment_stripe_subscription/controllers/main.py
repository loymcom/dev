import json
import logging
import pprint
import requests

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

# from odoo.addons.payment_stripe.const import HANDLED_WEBHOOK_EVENTS as ALREADY_HANDLED_WEBHOOK_EVENTS
from odoo.addons.payment_stripe.controllers.main import StripeController


_logger = logging.getLogger(__name__)

# HANDLED_WEBHOOK_EVENTS = ALREADY_HANDLED_WEBHOOK_EVENTS.extend(
#     [
HANDLED_WEBHOOK_EVENTS = [
        # payment_stripe
        # "payment_intent.amount_capturable_updated",
        # "payment_intent.succeeded",
        # "payment_intent.payment_failed",
        # "setup_intent.succeeded",
        # "charge.refunded",  # A refund has been issued.
        # "charge.refund.updated",  # The refund status has changed, possibly from succeeded to failed.
        #
        # payment_stripe_subscription
        "checkout.session.completed",
        "invoice.paid",
        "invoice.payment_failed",
    ]
# )


class StripeSubscriptionController(StripeController):

    @http.route(["/stripe_subscription"], type="http", auth="public")
    def stripe_subscription(self):
        return request.render("payment_stripe_subscription.stripe_subscription")
    
    @http.route("/stripe_subscrioption/create-checkout-session", type="http", auth="public", methods=["POST"])
    def stripe_create_checkout_session(self, file, import_id, jsonp="callback"):

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'success_url=http%3A%2F%2Flocalhost:16069%2Fstripe_subscription%2Fsuccess&line_items[0][price]=price_H5ggYwtDq4fbrJ&line_items[0][quantity]=2&mode=payment'
        

        response = requests.post(
            'https://api.stripe.com/v1/checkout/sessions',
            headers=headers,
            data=data,
            auth=('sk_test_FHDcKexlg9PsVFfZtOrnmds9', ''),
        )




    def stripe_webhook(self):
        """ Process the notification data sent by Stripe to the webhook.

        :return: An empty string to acknowledge the notification
        :rtype: str
        """
        event = json.loads(request.httprequest.data)
        _logger.info("notification received from Stripe with data:\n%s", pprint.pformat(event))
        try:
            if event["type"] in HANDLED_WEBHOOK_EVENTS:
                stripe_object = event["data"]["object"]  # {Payment,Setup}Intent, Charge, or Refund.

                # Check the integrity of the event.
                data = {
                    "reference": stripe_object.get("description"),
                    "event_type": event["type"],
                    "object_id": stripe_object["id"],
                }
                tx_sudo = request.env["payment.transaction"].sudo()._get_tx_from_notification_data(
                    "stripe", data
                )
                self._verify_notification_signature(tx_sudo)

                # Handle the notification data.
                if event["type"] == "checkout.session.completed":
                    pass
                elif event["type"] == "invoice.paid":
                    # Store the subscription.id and customer.id event objects in your database for verification.
                    pass
                elif event["type"] == "invoice.payment_failed":
                    pass

                if event["type"].startswith("payment_intent"):  # Payment operation.
                    self._include_payment_intent_in_notification_data(stripe_object, data)
                elif event["type"].startswith("setup_intent"):  # Validation operation.
                    # Fetch the missing PaymentMethod object.
                    payment_method = tx_sudo.provider_id._stripe_make_request(
                        f"payment_methods/{stripe_object['payment_method']}", method="GET"
                    )
                    _logger.info(
                        "received payment_methods response:\n%s", pprint.pformat(payment_method)
                    )
                    stripe_object["payment_method"] = payment_method
                    self._include_setup_intent_in_notification_data(stripe_object, data)
                elif event["type"] == "charge.refunded":  # Refund operation (refund creation).
                    refunds = stripe_object["refunds"]["data"]

                    # The refunds linked to this charge are paginated, fetch the remaining refunds.
                    has_more = stripe_object["refunds"]["has_more"]
                    while has_more:
                        payload = {
                            "charge": stripe_object["id"],
                            "starting_after": refunds[-1]["id"],
                            "limit": 100,
                        }
                        additional_refunds = tx_sudo.provider_id._stripe_make_request(
                            "refunds", payload=payload, method="GET"
                        )
                        refunds += additional_refunds["data"]
                        has_more = additional_refunds["has_more"]

                    # Process the refunds for which a refund transaction has not been created yet.
                    processed_refund_ids = tx_sudo.child_transaction_ids.filtered(
                        lambda tx: tx.operation == "refund"
                    ).mapped("provider_reference")
                    for refund in filter(lambda r: r["id"] not in processed_refund_ids, refunds):
                        refund_tx_sudo = self._create_refund_tx_from_refund(tx_sudo, refund)
                        self._include_refund_in_notification_data(refund, data)
                        refund_tx_sudo._handle_notification_data("stripe", data)
                    return ""  # Don't handle the notification data for the source transaction.
                elif event["type"] == "charge.refund.updated":  # Refund operation (with update).
                    # A refund was updated by Stripe after it was already processed (possibly to
                    # cancel it). This can happen when the customer's payment method can no longer
                    # be topped up (card expired, account closed...). The `tx_sudo` record is the
                    # refund transaction to update.
                    self._include_refund_in_notification_data(stripe_object, data)

                # Handle the notification data crafted with Stripe API objects
                tx_sudo._handle_notification_data("stripe", data)
            else:
                return super().stripe_webhook()
        except ValidationError:  # Acknowledge the notification to avoid getting spammed
            _logger.exception("unable to handle the notification data; skipping to acknowledge")
        return ""