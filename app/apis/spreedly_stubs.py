from flask import Response
from flask_restplus import Namespace, Resource

from app.fixtures.spreedly import deliver_data, export_data

spreedly_api = Namespace('spreedly', description='Spreedly related operations')


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
