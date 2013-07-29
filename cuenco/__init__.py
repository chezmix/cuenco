# all the imports
import os
from flask import Flask
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy

current_working_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# default configuration
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(current_working_directory, 'db/cuenco.sqlite3')
WEBSITE_URL = "http://localhost:5000"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('CUENCO_SETTINGS', silent=True)
db = SQLAlchemy(app)

  
def init_db():
    import cuenco.models
    db.create_all() 

import cuenco.views

if __name__ == '__main__':
    app.run()