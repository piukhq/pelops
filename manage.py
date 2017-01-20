#!/usr/bin/env python3
from flask.ext.script import Manager, Shell, Server
from app import create_app
import settings

app = create_app()
manager = Manager(app)

# access python shell with context
manager.add_command("shell", Shell(make_context=lambda: {'app': app}), use_ipython=True)

# run the app
manager.add_command("runserver", Server(port=settings.DEV_PORT, host=settings.DEV_HOST, threaded=True))

if __name__ == '__main__':
    manager.run()
