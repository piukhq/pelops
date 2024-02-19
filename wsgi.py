from pelops import create_app
from pelops.settings import settings

app = create_app(settings)


if __name__ == "__main__":
    app.run(settings.DEV_HOST, settings.DEV_PORT, debug=settings.DEBUG)
