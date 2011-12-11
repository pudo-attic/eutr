from bundle_config import config

SOLR_HOST = 'http://%s:%s%s' % (
        config['solr']['host'],
        config['solr']['port'],
        config['solr']['path'].rstrip('/'))
SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
        config['postgres']['username'],
        config['postgres']['password'],
        config['postgres']['host'],
        config['postgres']['port'],
        config['postgres']['database'])
