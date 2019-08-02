import json
from uuid import uuid4

from flask import request, jsonify, Response
from flask_restplus import Namespace, Resource

from app.fixtures.spreedly import deliver_data, export_data

spreedly_api = Namespace('spreedly', description='Spreedly related operations')

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
            with open(PAYMENT_TOKEN_FILEPATH, 'r') as f:
                file_data = json.loads(f.read())
        except (FileNotFoundError, json.JSONDecodeError):
            file_data = {"payment_tokens": [], "transaction_tokens": []}

        if request_json['transaction']['payment_method_token'] in file_data['payment_tokens']:
            resp = {
                "transaction": {
                    "token": str(uuid4()),
                    "succeeded": True
                }
            }
            try:
                with open(PAYMENT_TOKEN_FILEPATH, 'r') as f:
                    file_data = json.loads(f.read())
                    file_data['transaction_tokens'].append(resp['transaction']['token'])
            except (FileNotFoundError, json.JSONDecodeError):
                file_data = {
                    "payment_tokens": [],
                    "transaction_tokens": [resp['transaction']['token']]
                }

            with open(PAYMENT_TOKEN_FILEPATH, 'w+') as f:
                json.dump({"payment_tokens": file_data['payment_tokens'],
                           "transaction_tokens": file_data['transaction_tokens']}, f)
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
        try:
            with open(PAYMENT_TOKEN_FILEPATH, 'r') as f:
                file_data = json.loads(f.read())
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        if transaction_token in file_data['transaction_tokens']:
            resp = {"transaction": {"succeeded": True}}
        else:
            resp = {"transaction": {"succeeded": False}}

        return jsonify(resp)


@spreedly_api.route('/add_payment_token')
class AddPaymentToken(Resource):
    def post(self):
        tokens = request.get_json()['payment_tokens']
        tokens_added = []
        errors = []

        if isinstance(tokens, str):
            tokens = [tokens]

        try:
            with open(PAYMENT_TOKEN_FILEPATH, 'r') as f:
                file_data = json.loads(f.read())
        except (FileNotFoundError, json.JSONDecodeError):
            file_data = {"payment_tokens": [], "transaction_tokens": []}

        for token in tokens:
            if token not in file_data['payment_tokens']:
                file_data['payment_tokens'].append(token)
                tokens_added.append(token)
            else:
                errors.append("payment token '{}' already in valid tokens list".format(token))

        with open(PAYMENT_TOKEN_FILEPATH, 'w+') as f:
            json.dump({"payment_tokens": file_data['payment_tokens'],
                       "transaction_tokens": file_data['transaction_tokens']}, f)

        return jsonify({"tokens added": tokens_added, "errors": errors})
