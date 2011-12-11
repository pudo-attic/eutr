from flask import render_template, request, abort, url_for

from eutr.core import app, db
from eutr.model import Organisation
from eutr.pager import Pager

def _pager():
    return Pager(request.args, facets=['interests', 'subCategory', 'contactCountry'])

@app.route('/')
def index():
    return render_template('index.tmpl', pager=_pager())

@app.route('/search')
def search():
    return render_template('search.tmpl', pager=_pager())

@app.route('/org/<int:id>')
def organisation(id):
    organisation = db.session.query(Organisation).filter_by(id=id).first()
    if organisation is None:
        abort(404)
    from pprint import pformat
    raw = pformat(organisation.as_dict())
    return render_template('organisation.tmpl', 
            organisation=organisation, raw=raw)

if __name__ == "__main__":
    app.run(port=5009)

