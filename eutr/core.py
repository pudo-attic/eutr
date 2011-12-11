from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from solr import SolrConnection

from eutr import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)
try:
    app.config.from_object('eutr.production_settings')
except ImportError: pass

db = SQLAlchemy(app)

solr_host = app.config['SOLR_HOST']

def solr():
    return SolrConnection(solr_host)

