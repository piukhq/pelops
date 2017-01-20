from flask import Flask


def create_app(config_name="settings"):
    from app.apis import stub_api

    app = Flask('core')
    app.config.from_object(config_name)

    stub_api.init_app(app)

    return app
