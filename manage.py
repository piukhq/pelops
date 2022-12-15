#!/usr/bin/env python3
from sys import argv

from flask.cli import FlaskGroup

import settings
from app import create_app

app = create_app()
cli = FlaskGroup(app, load_dotenv=True)


@cli.command("example")
def run_server():
    print("example command issues")


if __name__ == "__main__":
    """
    note flask-script has been removed due to incompatibility with flask version 2

    to use in pycharm:
        Scipt path: full_path/PycharmProjects/pelops/manage.py
        parameters: as defined below for attribute with or without flags

    or for command line:
        pipenv run manage.py attribute

    attributes:

        runserver - For backward compatibility so we can use manage.py runserver which runs in debug mode using settings
                    and .env settings  -  No flags can be used

        otherwise runs cli which has built in commands and any added above like example:

                    - no attribute prints cli commands and flags
        routes      - list routes
        shell       - flask shell
        run         - as runserver but need to set your other parameters such as port otherwise uses 5000

    """
    try:
        if argv[1] == "runserver":
            app.run(settings.DEV_HOST, settings.DEV_PORT, debug=True)
    except (AttributeError, IndexError):
        pass
    print("cli starting")
    cli()
