from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from solr import SolrConnection

from eutr import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('EUTR_SETTINGS', silent=True)

db = SQLAlchemy(app)

solr_host = app.config['SOLR_HOST']

def solr():
    return SolrConnection(solr_host)

