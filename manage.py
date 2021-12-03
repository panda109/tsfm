# manage.py

#!/usr/bin/env python
import os
from app import create_app, db
from flask_script import Manager, Shell, Server
#from app.models import User
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash
from sqlalchemy.orm.dynamic import CollectionHistory

#from flask_uploads import UploadSet, IMAGES
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#images = UploadSet('images', IMAGES)
manager = Manager(app)


# server = Server(host="0.0.0.0", port=5000 , debug = True, ssl_context=context)
manager.add_command('db', MigrateCommand)
manager.add_command("http", Server(host="0.0.0.0", use_debugger=True, port=5000, use_reloader=True))
manager.add_command("https", Server(host="0.0.0.0", port=8100, ssl_crt='openssl/server.crt', ssl_key='openssl/server.key'))
# manager.add_command("https", Server(host="0.0.0.0",use_debugger=True,port = 443, use_reloader=True, ssl_context='adhoc'))


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def rebuild():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    manager.run()
