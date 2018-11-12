from flask import Flask

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware


def create_app(config_name="settings"):
    from app.apis import stub_api

    app = Flask('core')
    app.config.from_object(config_name)

    TraceMiddleware(
        app,
        tracer,
        service="pelops",
        distributed_tracing=True)

    stub_api.init_app(app)

    return app
