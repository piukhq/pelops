from flask_restplus import Namespace, Resource
from fixtures.spreedly import receiver_data

spreedly_api = Namespace('spreedly', description='Spreedly related operations')


@spreedly_api.route('/receivers/<slug>')
class SpreedlyStubs(Resource):
    def post(self, slug):
        return receiver_data[slug]
