from flask_restplus import Api, Resource
from flask import request
from app.apis.spreedly_stubs import spreedly_api as sp1
from settings import logger

stub_api = Api(ui=False,
               title="Bink Stubbing API - Pelops",
               version='1.0',
               description='Provides API endpoints for testing and staging environments',
               default='Pelops', default_label=u'Stubbed API for testing and staging')

stub_api.add_namespace(sp1)


class Healthz(Resource):
    def get(self):
        return ''


class VopActivate(Resource):

    def post(self):
        data = request.get_json()
        logger.info(f"request:  /vop/v1/activations/merchant  body: {data}")
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
        return {
            "correlationId": "96e38ed5-91d5-4567-82e9-6c441f4ca300",
            "responseDateTime": "2020-01-30T11:13:43.5765614Z",
            "responseStatus": {
                "code": "SUCCESS",
                "message": "Request proceed successfully without error."
            }
        }, 201


stub_api.add_resource(Healthz, '/healthz')
stub_api.add_resource(VopActivate, '/vop/v1/activations/merchant')
stub_api.add_resource(VopDeactivate, '/vop/v1/deactivations/merchant')