import json
from uuid import uuid4

from flask import request, jsonify, Response
from flask_restplus import Namespace, Resource

from app.apis.storage import Redis
from app.fixtures.spreedly import deliver_data, export_data
from settings import REDIS_URL
from settings import logger

from .psp_token import check_token

spreedly_api = Namespace('spreedly', description='Spreedly related operations')
storage = Redis(url=REDIS_URL)

DEFAULT_FILE_DATA = {"payment_tokens": [], "transaction_tokens": [], "void_fail_tokens": []}
PAYMENT_TOKEN_FILEPATH = 'app/fixtures/payment.json'
VOID_FAILURE_FLAG = "voidfail"


def spreedly_token_response(transaction_token, has_succeeded):
    return {
        "transaction": {
            "token": transaction_token,
            "succeeded": has_succeeded,
            "response": {
                "message": "",
                "error_code": 0
            }
        }
    }


def get_request_token(method, request_info):
    data = request.get_json()
    delivery = data.get('delivery', {})
    psp_token = delivery.get('payment_method_token', "")
    logger.info(f"{method} request {request_info}  body:{data}")
    return psp_token


@spreedly_api.route('/receivers/<token>/deliver.xml')
class Deliver(Resource):
    def post(self, token):
        if token in deliver_data:
            return Response(deliver_data[token], mimetype='text/xml')
        else:
            spreedly_api.abort(404, 'No deliver data for token {}'.format(token))


@spreedly_api.route('/receivers/<token>/deliver.json')
class DeliverJson(Resource):
    def post(self, token):
        if token == 'visa':
            psp_token = get_request_token('POST', f'/receivers/{token}/deliver.json')
            active, error_type, code, unique_token = check_token('ADD', psp_token)
            if active:
                if error_type:
                    resp_data = deliver_data['visa_error']
                    resp_data["transaction"]["response"]["body"] = resp_data["transaction"]["response"]["body"]\
                        .replace("<<error>>", code)
                    return Response(json.dumps(resp_data), mimetype='application/json')
                else:
                    if not code:
                        code = 404
                    spreedly_api.abort(code, f'No deliver data for Visa simulated psp token {unique_token}'
                                             f' - psp token in request {psp_token}')
            else:
                return Response(json.dumps(deliver_data[token]), mimetype='application/json')
        else:
            spreedly_api.abort(404, 'request made to deliver.json requires a visa token i.e. '
                                    'Pelops only supports json format for VISA (VOP)')


@spreedly_api.route('/receivers/<token>/export.xml')
class Export(Resource):
    def post(self, token):
        if token in export_data:
            return Response(export_data[token], mimetype='text/xml')
        else:
            spreedly_api.abort(404, 'No export data for token {}'.format(token))


@spreedly_api.route('/payment_methods/<psp_token>/retain.json')
class Retain(Resource):
    def put(self, psp_token):
        active, error_type, code, _ = check_token('RET', psp_token)
        if not active:
            return True
        else:
            if error_type:      # We want to ignore payment error strings if set for retain ie we might use xxx
                code = 404
            spreedly_api.abort(code, f'Not retained token {psp_token}')
            logger.info(f"Spreedly api Abort {code} - token {psp_token} not retained")


@spreedly_api.route('/v1/gateways/<gateway_token>/purchase.json')
class PaymentPurchase(Resource):
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
            file_data = DEFAULT_FILE_DATA

        if input_payment_token in file_data['payment_tokens']:
            transaction_token = str(uuid4())
            resp = spreedly_token_response(transaction_token, has_succeeded=True)
            file_data = {
                "payment_tokens": [],
                "transaction_tokens": [transaction_token],
                "void_fail_tokens": []
            }
            if input_payment_token == VOID_FAILURE_FLAG:
                file_data['void_fail_tokens'] = [transaction_token]
            storage.set(
                token_storage_key,
                json.dumps(file_data)
            )
        else:
            resp = spreedly_token_response(str(uuid4()), has_succeeded=False)

        return jsonify(resp)


@spreedly_api.route('/v1/transactions/<transaction_token>/void.json')
class PaymentVoid(Resource):
    def post(self, transaction_token):
        token_storage_key = 'tokens'
        try:
            file_data = json.loads(storage.get(token_storage_key))
        except (json.JSONDecodeError, storage.NotFound):
            file_data = DEFAULT_FILE_DATA

        void_fail = transaction_token in file_data["void_fail_tokens"]
        if transaction_token in file_data["transaction_tokens"] and not void_fail:
            resp = {
                "transaction": {
                    "succeeded": True,
                    "response": {
                        "message": "",
                        "error_code": 0
                    }
                }
            }
        else:
            resp = {
                "transaction": {
                    "succeeded": False,
                    "response": {
                        "message": "",
                        "error_code": 0
                    }
                }
            }

        return jsonify(resp)


@spreedly_api.route('/add_payment_token')
class AddPaymentToken(Resource):
    def post(self):
        try:
            tokens = request.get_json()['payment_tokens']
        except KeyError:
            return jsonify({"message": "incorrect input format"})
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
