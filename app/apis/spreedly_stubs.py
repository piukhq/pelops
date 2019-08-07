import json
from uuid import uuid4

from flask import request, jsonify, Response
from flask_restplus import Namespace, Resource

from app.apis.storage import Redis
from app.fixtures.spreedly import deliver_data, export_data
from settings import REDIS_URL

spreedly_api = Namespace('spreedly', description='Spreedly related operations')
storage = Redis(url=REDIS_URL)

PAYMENT_TOKEN_FILEPATH = 'app/fixtures/payment.json'


@spreedly_api.route('/receivers/<token>/deliver.xml')
class Deliver(Resource):
    def post(self, token):
        if token in deliver_data:
            return Response(deliver_data[token], mimetype='text/xml')
        else:
            spreedly_api.abort(404, 'No deliver data for token {}'.format(token))


@spreedly_api.route('/receivers/<token>/export.xml')
class Export(Resource):
    def post(self, token):
        if token in export_data:
            return Response(export_data[token], mimetype='text/xml')
        else:
            spreedly_api.abort(404, 'No export data for token {}'.format(token))


@spreedly_api.route('/payment_methods/<token>/retain.json')
class Retain(Resource):
    def put(self, token):
        if token:
            return True
        else:
            spreedly_api.abort(404, 'Not retained token {}'.format(token))


@spreedly_api.route('/v1/gateways/<gateway_token>/authorize.json')
class PaymentAuthorisation(Resource):
    def post(self, gateway_token):
        request_json = request.get_json()

        try:
            input_payment_token = request_json['transaction']['payment_method_token']
        except KeyError:
            return jsonify({"message": "incorrect input format"})

        token_storage_key = 'tokens'
        try:
            file_data = json.loads(storage.get(token_storage_key))
        except (json.JSONDecodeError, storage.NotFound):
            file_data = {"payment_tokens": [], "transaction_tokens": []}

        if input_payment_token in file_data['payment_tokens']:
            resp = {
                "transaction": {
                    "token": str(uuid4()),
                    "succeeded": True
                }
            }
            file_data['transaction_tokens'].append(resp['transaction']['token'])
            file_data = {
                "payment_tokens": [],
                "transaction_tokens": [resp['transaction']['token']]
            }
            storage.set(
                token_storage_key,
                json.dumps({"payment_tokens": file_data['payment_tokens'],
                            "transaction_tokens": file_data['transaction_tokens']})
            )
        else:
            resp = {
                "transaction": {
                    "token": str(uuid4()),
                    "succeeded": False
                }
            }

        return jsonify(resp)


@spreedly_api.route('/v1/transactions/<transaction_token>/void.json')
class PaymentVoid(Resource):
    def post(self, transaction_token):
        token_storage_key = 'tokens'
        try:
            file_data = json.loads(storage.get(token_storage_key))
        except (json.JSONDecodeError, storage.NotFound):
            file_data = {"payment_tokens": [], "transaction_tokens": []}

        if transaction_token in file_data['transaction_tokens']:
            resp = {"transaction": {"succeeded": True}}
        else:
            resp = {"transaction": {"succeeded": False}}

        return jsonify(resp)


@spreedly_api.route('/add_payment_token')
class AddPaymentToken(Resource):
    def post(self):
        tokens = request.get_json()['payment_tokens']
        token_storage_key = 'tokens'
        tokens_added = []
        errors = []

        if isinstance(tokens, str):
            tokens = [tokens]

        try:
            file_data = json.loads(storage.get(token_storage_key))
        except (json.JSONDecodeError, storage.NotFound):
            file_data = {"payment_tokens": [], "transaction_tokens": []}

        for token in tokens:
            if token not in file_data['payment_tokens']:
                file_data['payment_tokens'].append(token)
                tokens_added.append(token)
            else:
                errors.append("payment token '{}' already in valid tokens list".format(token))

        storage.set(
            token_storage_key,
            json.dumps({"payment_tokens": file_data['payment_tokens'],
                       "transaction_tokens": file_data['transaction_tokens']})
        )

        return jsonify({"tokens added": tokens_added, "errors": errors})
