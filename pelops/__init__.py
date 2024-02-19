from flask import Flask


def create_app(config: object) -> Flask:
    from pelops.apis import stub_api

    app = Flask("core")
    app.config.from_object(config)

    stub_api.init_app(app)

    return app
