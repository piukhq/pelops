import redis
from flask import request
from flask_restplus import Api, Resource
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

from app.apis.spreedly_stubs import spreedly_api as sp1
from settings import REDIS_URL, logger
from .psp_token import check_token
from .storage import Redis
from settings import AUTH_USERNAME, AUTH_PASSWORD

auth = HTTPBasicAuth()
users = {AUTH_USERNAME: generate_password_hash(AUTH_PASSWORD)}

storage = Redis(url=REDIS_URL)

stub_api = Api(
    ui=False,
    title="Bink Stubbing API - Pelops",
    version="1.0",
    description="Provides API endpoints for testing and staging environments",
    default="Pelops",
    default_label="Stubbed API for testing and staging",
)

stub_api.add_namespace(sp1)


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


class Healthz(Resource):
    def get(self):
        return ""


class Readyz(Resource):
    def get(self):
        try:
            r = redis.Redis.from_url(REDIS_URL)
            r.ping()
            return "", 204
        except Exception as err:
            return {"error": str(err)}, 500


class Livez(Resource):
    def get(self):
        return "", 204


class VopActivate(Resource):

    def post(self):
        data = request.get_json()
        logger.info(f"request:  /vop/v1/activations/merchant  body: {data}")
        user_key = data.get('userKey')
        active, error_type, code, unique_token = check_token('ACT', user_key)
        if active:
            if error_type:
                return {
                           "activationId": "88395654-0b8a-4f2d-9046-2b8669f76bd2",
                           "correlationId": "96e38ed5-91d5-4567-82e9-6c441f4ca300",
                           "responseDateTime": "2020-01-30T11:13:43.5765614Z",
                           "responseStatus": {
                               "code": code,
                               "message": "VOP Activate failure message.",
                               "responseStatusDetails": []
                           }
                       }, 200
            else:
                if not code:
                    code = 500
                sp1.abort(code, f"Failed VOP Activation request for {unique_token}")

        else:
            return {
                       "activationId": "88395654-0b8a-4f2d-9046-2b8669f76bd2",
                       "correlationId": "96e38ed5-91d5-4567-82e9-6c441f4ca300",
                       "responseDateTime": "2020-01-30T11:13:43.5765614Z",
                       "responseStatus": {
                           "code": "SUCCESS",
                           "message": "Request proceed successfully without error."
                       }
                   }, 201


class VopDeactivate(Resource):

    def post(self):
        data = request.get_json()
        logger.info(f"request:  vop/v1/deactivations/merchant  body: {data}")
        user_key = data.get('userKey')
        active, error_type, code, unique_token = check_token('DEACT', user_key)
        if active:
            if error_type:
                return {
                           "activationId": "88395654-0b8a-4f2d-9046-2b8669f76bd2",
                           "correlationId": "96e38ed5-91d5-4567-82e9-6c441f4ca300",
                           "responseDateTime": "2020-01-30T11:13:43.5765614Z",
                           "responseStatus": {
                               "code": code,
                               "message": "VOP DeActivate failure message.",
                               "responseStatusDetails": []
                           }
                       }, 200
            else:
                if not code:
                    code = 500
                sp1.abort(code, f"Failed VOP DeActivation request for {unique_token}")

        else:
            return {
                "correlationId": "96e38ed5-91d5-4567-82e9-6c441f4ca300",
                "responseDateTime": "2020-01-30T11:13:43.5765614Z",
                "responseStatus": {
                    "code": "SUCCESS",
                    "message": "Request proceed successfully without error."
                }
            }, 201


class VopUnenroll(Resource):

    def post(self):
        data = request.get_json()
        logger.info(f"request:  /vop/v1/users/unenroll  body: {data}")
        if data:
            user_key = data.get('userKey')
            active, error_type, code, unique_token = check_token('DEL', user_key)
            if active:
                if error_type:
                    return {
                               "correlationId": "ce708e6a-fd5f-48cc-b9ff-ce518a6fda1a",
                               "responseDateTime": "2020-01-29T15:02:50.8109336Z",
                               "responseStatus": {
                                   "code": code,
                                   "message": "VOP Unenroll failure message.",
                                   "responseStatusDetails": []
                               }
                           }, 200
                else:
                    if not code:
                        code = 404
                    sp1.abort(code, f"Failed VOP Unenrol request for {unique_token}")

            else:
                per, success, message, err, err_message = storage.update_if_per(user_key, 'DELETED', 'visa')
                if per and not success:
                    return {
                               "correlationId": "ce708e6a-fd5f-48cc-b9ff-ce518a6fda1a",
                               "responseDateTime": "2020-01-29T15:02:50.8109336Z",
                               "responseStatus": {
                                   "code": err,
                                   "message": err_message,
                                   "responseStatusDetails": []
                               }
                           }, 200
                else:
                    return {
                        "correlationId": "ce708e6a-fd5f-48cc-b9ff-ce518a6fda1a",
                        "responseDateTime": "2020-01-29T15:02:50.8109336Z",
                        "responseStatus": {
                            "code": "SUCCESS",
                            "message": "Request proceed successfully without error."
                        }
                    }, 201
        else:
            sp1.abort(400, "Invalid request")


class CardStatus(Resource):

    @auth.login_required
    def get(self, psp_token):
        try:
            status = storage.get(f'card_{psp_token}')
        except storage.NotFound:
            return {
                       "Token": psp_token,
                       "Message": "No card data found"
                   }, 404

        try:
            log_str = storage.rlist_to_list(f'cardlog_{psp_token}')
        except storage.NotFound:
            log_str = 'No log available'

        return {
                    "Token": psp_token,
                    "Card status": status,
                    "Log": log_str
                }, 200


class AmexOauth(Resource):

    def post(self):
        data = request.get_json()
        logger.info(f"amex oath: /apiplatform/v2/oauth/token/mac  body: {data}")
        return {
                   "access_token": "Pelops_Amex_test_token",
                   "mac_key": "Pelops_Amex_Mac_key"
               }, 201


stub_api.add_resource(Healthz, "/healthz")
stub_api.add_resource(Readyz, "/readyz")
stub_api.add_resource(Livez, "/livez")
stub_api.add_resource(VopActivate, "/vop/v1/activations/merchant")
stub_api.add_resource(VopDeactivate, "/vop/v1/deactivations/merchant")
stub_api.add_resource(VopUnenroll, "/vop/v1/users/unenroll")
stub_api.add_resource(CardStatus, "/cardstatus/<psp_token>")
stub_api.add_resource(AmexOauth, "/apiplatform/v2/oauth/token/mac")
