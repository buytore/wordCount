__author__ = 'mbannan'

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import app, db

#filename = os.path.join(app.instance_path, 'application.cfg')
#with open(filename) as f:
#    config = f.read()

#app.config.from_object(os.environ['APP_SETTINGS'])

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/wordcount_dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Howdy1@localhost/wordcount_dev'

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
