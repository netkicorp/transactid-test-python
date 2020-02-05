import datetime
import requests

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for

from transactid.transactid import TransactID
from transactid.exceptions import InvalidSignatureException
from transactid.exceptions import DecodeException
from dummy_keys import DUMMY_PRIVATE_KEY
from dummy_keys import DUMMY_CERT

# this would need to be created for each individual client using their private key and certificate
transact = TransactID(private_key_pem=DUMMY_PRIVATE_KEY, certificate_pem=DUMMY_CERT)


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/initial-invoice-request")
def initial_invoice_request():
    """
    * amount: Optional[int]  # amount is integer-number-of-satoshis
    * pki_type: Optional[str]  # Currently only x509+sha256 and the string none are supported.
    * memo: Optional[str]
    * notification_url: Optional[str]
    """
    serialized_invoice_request = transact.create_invoice_request(
        pki_type="x509+sha256",
        memo="This is a demo request.",
        notification_url=url_for("payment_request", _external=True)
    )

    url = request.args.get("url")
    if url:
        r = requests.post(url, data=serialized_invoice_request)
        return f"response from {url} was {r.status_code}"
    else:
        return serialized_invoice_request


@app.route("/invoice-request", methods=["POST"])
def invoice_request():
    """
    * time_stamp: datetime
    * outputs: List[(int, bytes)]  # int: amount, bytes: script (see BIP70 details for more information on scripts)
    * memo: str
    * payment_url: str
    * merchant_data: bytes
    * expires: Optional[datetime]
    * pki_type: Optional[str]
    * network: str, defaults to "main"
    * payment_details_version: int, defaults to 1
    """
    try:
        transact.verify_invoice_request(request.data)
    except InvalidSignatureException:
        return "Invalid Signature received"
    except DecodeException:
        return "Unable to decode protobuf object"
    else:
        invoice_request = transact.get_verified_invoice_request()
        app.logger.info(invoice_request)
        # here is where you would normally do business logic against the data you received
        serialized_payment_request = transact.create_payment_request(
            time_stamp=datetime.datetime.now(),
            outputs=[(2052020, b"stan LOONA")],  # you would normally put a regular blockchain script here
            memo=invoice_request["memo"],
            payment_url=url_for("payment", _external=True),
            merchant_data=b"merchant identifier goes here (optional)",
            pki_type="x509+sha256"
        )

        return serialized_payment_request


@app.route("/payment-request", methods=["POST"])
def payment_request():
    """
    * transactions: List[bytes]
    * refund_to: List[(int, bytes)]  # int: amount, bytes: script (see BIP70 details for more information on scripts)
    * merchant_data: Optional[bytes]
    * memo: Optional[str]
    """
    try:
        transact.verify_payment_request(request.data)
    except InvalidSignatureException:
        return "Invalid Signature received"
    except DecodeException:
        return "Unable to decode protobuf object"
    else:
        payment_request = transact.get_verified_payment_request()
        app.logger.info(payment_request)
        # here is where you would normally do business logic against the data you received

        serialized_payment = transact.create_payment(
            transactions=[b"blockchain transactions go here"],
            refund_to=[(2052020, b"stan LOONA")],  # you would normally put a regular blockchain script here
            memo="here's your payment",
            merchant_data=b"merchant identifier goes here (optional)",
        )
        return serialized_payment


@app.route("/payment", methods=["POST"])
def payment():

    try:
        transact.verify_payment(request.data)
    except DecodeException:
        return "Unable to decode protobuf object"
    else:
        payment = transact.get_verified_payment()
        app.logger.info(payment)
        # here is where you would normally do business logic against the data you received
        serialized_payment_ack = transact.create_payment_ack(memo="thanks for the coin chummer")

        return serialized_payment_ack
