from flask_restplus import Namespace, Resource

from app.fixtures.spreedly import deliver_data, export_data

spreedly_api = Namespace('spreedly', description='Spreedly related operations')


@spreedly_api.route('/receivers/<token>/deliver.xml')
class Deliver(Resource):
    def post(self, token):
        if token in deliver_data:
            return deliver_data[token]
        else:
            spreedly_api.abort(404, 'No deliver data for token {}'.format(token))


@spreedly_api.route('/receivers/<token>/export.xml')
class Export(Resource):
    def post(self, token):
        if token in export_data:
            return export_data[token]
        else:
            spreedly_api.abort(404, 'No export data for token {}'.format(token))
