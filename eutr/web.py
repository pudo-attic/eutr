from flask import render_template, request, abort, url_for

from eutr.core import app, db
from eutr.model import Organisation
from eutr.pager import Pager

@app.route('/')
def index():
    pager = Pager(request.args, facets=['interests', 'actionType'])
    return render_template('index.tmpl', pager=pager)

@app.route('/search')
def search():
    pager = Pager(request.args, facets=['interests', 'actionType'])
    return render_template('search.tmpl', pager=pager)

@app.route('/org/<int:id>')
def organisation(id):
    organisation = db.session.query(Organisation).filter_by(id=id).first()
    if organisation is None:
        abort(404)
    return render_template('organisation.tmpl', 
            organisation=organisation)

if __name__ == "__main__":
    app.run(port=5009)

