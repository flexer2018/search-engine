from flask import Flask, g, request, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'searchengine.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def index():
    return render_template('index.html', title = 'Home')

@app.route("/search-results/")
def search_results():
    search_input = request.args.get('search_input')
    cur = get_db().cursor()
    cur.execute("SELECT domain FROM domains WHERE domain LIKE ?", ['%' + search_input + '%'])
    results = cur.fetchall()
    return render_template('search_results.html', title='Search Results', results=results)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()