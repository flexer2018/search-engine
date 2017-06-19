from flask import Flask, g, request, render_template
import re, sqlite3

app = Flask(__name__)
DATABASE = 'searchengine.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.route("/")
def index():
    return render_template('index.html', title='Home', search_input='')

@app.route("/search-results/")
def search_results():
    search_input = request.args.get('search_input')
    cur = get_db().cursor()
    cur.execute("SELECT * FROM pages WHERE content LIKE ?", ['%' + search_input + '%'])
    results = cur.fetchall()
    results_display = []
    for result in results:
        result_display = dict(result)
        match = re.search(search_input, result_display['content'], re.IGNORECASE)
        if match is not None:
            result_display['text_before'] = result_display['content'][match.span(0)[0] - 100:match.span(0)[0]]
            result_display['search_input'] = result_display['content'][match.span(0)[0]:match.span(0)[1]]
            result_display['text_after'] = result_display['content'][match.span(0)[1]:match.span(0)[1] + 100]
            results_display.append(result_display)

    # print(results_display)
    return render_template('search_results.html', title='Search Results', search_input=search_input, results=results_display)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()