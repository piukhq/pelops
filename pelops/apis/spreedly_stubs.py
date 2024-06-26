import json
import re
from typing import Literal, cast
from uuid import uuid4

from flask import Response, jsonify, request
from flask_restx import Namespace, Resource
from loguru import logger

from pelops.apis.storage import Redis
from pelops.fixtures.spreedly import deliver_data, export_data
from pelops.settings import settings

from .psp_token import check_token

spreedly_api = Namespace("spreedly", description="Spreedly related operations")
storage = Redis(url=settings.REDIS_URL)

DEFAULT_FILE_DATA: dict[str, list] = {
    "payment_tokens": [],
    "transaction_tokens": [],
    "void_fail_tokens": [],
}
PAYMENT_TOKEN_FILEPATH = "app/fixtures/payment.json"
VOID_FAILURE_FLAG = "voidfail"


def check_and_send(  # type: ignore [return]  # noqa: PLR0913
    per: bool,
    err: str,
    success: bool,
    spreedly_agent_receiver_token: Literal["visa", "amex", "mastercard"],
    psp_token: str,
    err_message: str,
) -> Response:
    # Checks for persistence, and if so then sends success or fail response in line with persistence logic (see
    # storage.update_if_per()). Also populates psp_tokens, error codes and error messages as necessary.
    if spreedly_agent_receiver_token in ("amex", "mastercard"):
        is_error = bool(per and not success)

        return Response(
            Deliver.populate_xml_with_data(
                spreedly_agent_receiver_token,
                code=err,
                psp_token=psp_token,
                err_message=err_message,
                is_error=is_error,
            ),
            mimetype="text/xml",
        )

    elif spreedly_agent_receiver_token == "visa":
        if per and not success:
            resp_data = deliver_data["visa_error"].copy()
            resp_data["transaction"]["response"]["body"] = (
                resp_data["transaction"]["response"]["body"]
                .replace("<<error>>", err)
                .replace("<<errormessage>>", err_message)
            )
            resp_data["transaction"]["payment_method"]["token"] = psp_token
        else:
            resp_data = deliver_data[spreedly_agent_receiver_token].copy()
            resp_data["transaction"]["response"]["body"] = resp_data["transaction"]["response"]["body"].replace(
                "<<TOKEN>>", psp_token
            )
        return Response(json.dumps(resp_data), mimetype="application/json")


def spreedly_token_response(transaction_token: str, has_succeeded: bool) -> dict:
    return {
        "transaction": {
            "token": transaction_token,
            "succeeded": has_succeeded,
            "response": {"message": "", "error_code": 0},
        }
    }


@spreedly_api.route("/receivers/<spreedly_agent_receiver_token>/deliver.xml")
class Deliver(Resource):
    def post(
        self,
        spreedly_agent_receiver_token: Literal["visa", "mastercard", "amex"],
    ) -> Response:
        # spreedly_agent_receiver_token is sent to Pelops as 'amex', 'visa' or 'mastercard'. In prod this would be a
        # more traditional token which Spreedly would use to connect with the correct agent.
        logger.info("request  /receivers/{}/deliver.xml", spreedly_agent_receiver_token)
        if spreedly_agent_receiver_token in deliver_data:
            if spreedly_agent_receiver_token in ("amex", "mastercard"):
                data = request.data.decode("utf8")
                psp_token = self.get_xml_request_token(
                    "POST",
                    f"/receivers/{spreedly_agent_receiver_token}/deliver.xml",
                    data,
                )
                action = self.get_xml_action_code(data, spreedly_agent_receiver_token)

                # Checks for ERR or REQ codes and if found strips down the token and enacts retries/error simulation.
                err_sim_active, psp_error_code, err_code, unique_token = check_token(action, psp_token)
                if err_sim_active:
                    if psp_error_code:
                        resp_data = self.populate_xml_with_data(
                            spreedly_agent_receiver_token,
                            err_code,
                            psp_token,
                            is_error=True,
                        )
                        return Response(resp_data, mimetype="text/xml")
                    else:
                        if not err_code:
                            err_code = 404

                        message = f"Pelops-generated error for psp_token: " f"{unique_token}"
                        errors = {"errors": [{"message": message}]}
                        return Response(
                            json.dumps(errors),
                            mimetype="application/json",
                            status=err_code,
                        )

                # Checks for PER prefix and if found updates persistence layer
                per, success, message, err, err_message = storage.update_if_per(
                    psp_token, action, spreedly_agent_receiver_token
                )
                return check_and_send(
                    per,
                    err,
                    success,
                    spreedly_agent_receiver_token,
                    psp_token,
                    err_message,
                )
            else:
                return Response(deliver_data[spreedly_agent_receiver_token], mimetype="text/xml")

        else:
            spreedly_api.abort(
                404,
                f"No deliver data in request for {spreedly_agent_receiver_token}",
            )

    @staticmethod
    def get_xml_action_code(request_data: str, spreedly_agent_receiver_token: str) -> str:
        # Searches for string and determines if request is for enrolment or unenrolment
        if spreedly_agent_receiver_token == "mastercard":
            search_pattern = "<cus:ACCOUNT_STATUS_ID>3"
        else:
            search_pattern = "unsync_details"

        action = "DEL" if search_pattern in request_data else "ADD"

        return action

    @staticmethod
    def get_xml_request_token(method: str, request_info: str, data: str) -> str:
        # Extracts psp_token from XML request
        result = re.search("<payment_method_token>(.*)</payment_method_token>", data)
        if not result:
            raise ValueError(f"Failed to extract psp_token from {method} request {request_info}  body:{data}")
        psp_token = result.group(1)
        logger.info("{} psp_token: {} request {}", method, psp_token, request_info)

        return psp_token

    @staticmethod
    def populate_xml_with_data(
        spreedly_agent_receiver_token: Literal["visa", "amex", "mastercard"],
        code: int | str,
        psp_token: str,
        err_message: str | None = None,
        is_error: bool = False,
    ) -> str:
        # Replaces placeholders in responses with accurate token and error information.
        if err_message is None:
            err_message = "Pelops-generated error"
        replace_list = {
            "<<error>>": str(code),
            "<<errormessage>>": err_message,
            "<<TOKEN>>": psp_token,
        }

        if is_error:
            resp_text = deliver_data.copy()[spreedly_agent_receiver_token + "_error"]  # type: ignore [literal-required]
        else:
            resp_text = deliver_data.copy()[spreedly_agent_receiver_token]

        for key, value in replace_list.items():
            resp_text = resp_text.replace(key, value)
        return resp_text


@spreedly_api.route("/receivers/<spreedly_agent_receiver_token>/deliver.json")
class DeliverJson(Resource):
    def post(  # type: ignore [return]
        self,
        spreedly_agent_receiver_token: Literal["visa", "mastercard", "amex"],
    ) -> Response:
        if spreedly_agent_receiver_token == "visa":
            psp_token = self.get_json_request_token("POST", f"/receivers/{spreedly_agent_receiver_token}/deliver.json")
            active, error_type, err_code, unique_token = check_token("ADD", psp_token)
            if active:
                if error_type:
                    resp_data = cast(dict, deliver_data["visa_error"])
                    resp_data["transaction"]["response"]["body"] = resp_data["transaction"]["response"]["body"].replace(
                        "<<error>>", err_code
                    )
                    resp_data["transaction"]["payment_method"]["token"] = psp_token
                    return Response(json.dumps(resp_data), mimetype="application/json")
                else:
                    if not err_code:
                        err_code = 404
                    spreedly_api.abort(
                        err_code,
                        f"Pelops-generated error for psp_token: {unique_token}",
                    )
            else:
                per, success, message, err, err_message = storage.update_if_per(
                    psp_token, "ADD", spreedly_agent_receiver_token
                )
                return check_and_send(
                    per,
                    err,
                    success,
                    spreedly_agent_receiver_token,
                    psp_token,
                    err_message,
                )
        else:
            spreedly_api.abort(
                404,
                "Pelops' deliver.json endpoint currently only supports calls for VOP (Visa) cards. "
                "Please use /receivers/visa/deliver.json",
            )

    @staticmethod
    def get_json_request_token(method: str, request_info: str) -> str:
        # Extracts psp_token from JSON request
        data = request.get_json()
        delivery = data.get("delivery", {})
        psp_token = delivery.get("payment_method_token", "")
        logger.info("{} request {}  body:{}", method, request_info, data)
        return psp_token


@spreedly_api.route("/receivers/<spreedly_agent_receiver_token>/export.xml")
class Export(Resource):
    def post(self, spreedly_agent_receiver_token: str) -> Response:  # type: ignore [return]
        if spreedly_agent_receiver_token in export_data:
            return Response(export_data[spreedly_agent_receiver_token], mimetype="text/xml")
        else:
            spreedly_api.abort(404, f"No export data for {spreedly_agent_receiver_token}")


@spreedly_api.route("/payment_methods/<psp_token>/retain.json")
class Retain(Resource):
    def put(self, psp_token: str) -> bool | None:  # type: ignore [return]
        active, error_type, code, unique_code = check_token("RET", psp_token)
        if not active:
            storage.update_if_per(psp_token, "RET", "")
            return True

        if error_type:  # We want to ignore payment error strings if set for retain ie we might use xxx
            code = 404

        spreedly_api.abort(code, f"Not retained token {psp_token}")
        logger.info("Spreedly api Abort {} - token {psp_token} not retained", code)


@spreedly_api.route("/payment_methods/<psp_token>/redact.json")
class Redact(Resource):
    def put(self, psp_token: str) -> Response:
        logger.info("request  /payment_methods/{}/redact.json", psp_token)
        resp = spreedly_token_response(str(uuid4()), has_succeeded=True)
        return jsonify(resp)


@spreedly_api.route("/v1/gateways/<gateway_token>/purchase.json")
class PaymentPurchase(Resource):
    def post(self, gateway_token: str) -> Response:  # noqa: ARG002
        request_json = request.get_json()

        try:
            input_payment_token = request_json["transaction"]["payment_method_token"]
        except KeyError:
            return jsonify({"message": "incorrect input format"})

        token_storage_key = "tokens"
        try:
            file_data = json.loads(storage.get(token_storage_key))
        except (json.JSONDecodeError, storage.NotFound):
            file_data = DEFAULT_FILE_DATA

        if input_payment_token in file_data["payment_tokens"]:
            transaction_token = str(uuid4())
            resp = spreedly_token_response(transaction_token, has_succeeded=True)
            file_data = {
                "payment_tokens": [],
                "transaction_tokens": [transaction_token],
                "void_fail_tokens": [],
            }
            if input_payment_token == VOID_FAILURE_FLAG:
                file_data["void_fail_tokens"] = [transaction_token]
            storage.set(token_storage_key, json.dumps(file_data))
        else:
            resp = spreedly_token_response(str(uuid4()), has_succeeded=False)

        return jsonify(resp)


@spreedly_api.route("/v1/transactions/<transaction_token>/void.json")
class PaymentVoid(Resource):
    def post(self, transaction_token: str) -> Response:
        token_storage_key = "tokens"
        try:
            file_data = json.loads(storage.get(token_storage_key))
        except (json.JSONDecodeError, storage.NotFound):
            file_data = DEFAULT_FILE_DATA

        void_fail = transaction_token in file_data["void_fail_tokens"]
        if transaction_token in file_data["transaction_tokens"] and not void_fail:
            resp = {
                "transaction": {
                    "succeeded": True,
                    "response": {"message": "", "error_code": 0},
                }
            }
        else:
            resp = {
                "transaction": {
                    "succeeded": False,
                    "response": {"message": "", "error_code": 0},
                }
            }

        return jsonify(resp)


@spreedly_api.route("/add_payment_token")
class AddPaymentToken(Resource):
    def post(self) -> Response:
        try:
            tokens = request.get_json()["payment_tokens"]
        except KeyError:
            return jsonify({"message": "incorrect input format"})
        token_storage_key = "tokens"
        tokens_added = []
        errors = []

        if isinstance(tokens, str):
            tokens = [tokens]

        try:
            file_data = json.loads(storage.get(token_storage_key))
        except (json.JSONDecodeError, storage.NotFound):
            file_data = {"payment_tokens": [], "transaction_tokens": []}

        for token in tokens:
            if token not in file_data["payment_tokens"]:
                file_data["payment_tokens"].append(token)
                tokens_added.append(token)
            else:
                errors.append(f"payment token '{token}' already in valid tokens list")

        storage.set(
            token_storage_key,
            json.dumps(
                {
                    "payment_tokens": file_data["payment_tokens"],
                    "transaction_tokens": file_data["transaction_tokens"],
                }
            ),
        )

        return jsonify({"tokens added": tokens_added, "errors": errors})
