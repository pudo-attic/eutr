from flask import render_template, request, abort, url_for

from eutr.core import app, db
from eutr.model import Entity
from eutr.pager import Pager

def _pager():
    return Pager(request.args, facets=['interests', 'subCategory', 'contactCountry'])

@app.route('/')
def index():
    return render_template('index.tmpl', pager=_pager())

@app.route('/search')
def search():
    return render_template('search.tmpl', pager=_pager())

@app.route('/entity/<int:id>')
def entity(id):
    entity = db.session.query(Entity).filter_by(id=id).first()
    if entity is None:
        abort(404)
    from pprint import pformat
    raw = pformat(entity.as_dict())
    return render_template('entity.tmpl', 
            entity=entity, raw=raw)

if __name__ == "__main__":
    app.run(port=5009)

