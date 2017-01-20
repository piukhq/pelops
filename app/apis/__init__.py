from flask_restplus import Api
from app.apis.spreedly_stubs import spreedly_api as sp1

stub_api = Api(ui=False,
               title="Bink Stubbing API - Pelops",
               version='1.0',
               description='Provides API endpoints for testing and staging environments',
               default='Pelops', default_label=u'Stubbed API for testing and staging')

stub_api.add_namespace(sp1)
