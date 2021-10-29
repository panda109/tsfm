# wsgi.py
#gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
#!/usr/bin/env python
import os
from app import create_app
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# server = Server(host="0.0.0.0", port=5000 , debug = True, ssl_context=context) test github
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Catalog=Catalog)

if __name__ == '__main__':
    app.run()
~                      