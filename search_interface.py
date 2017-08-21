import re, sqlite3
from elasticsearch import Elasticsearch
from flask import Flask, g, request, render_template
# from whoosh.query import *
# from whoosh.qparser import QueryParser

app = Flask(__name__)
DATABASE = 'searchengine.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def get_domains():
    cur = get_db().cursor()
    cur.execute("SELECT id, domain FROM domains")
    domains = [dict(row) for row in cur.fetchall()]
    return domains

@app.route("/")
def index():
    cur = get_db().cursor()
    cur.execute("SELECT id, domain FROM domains")
    domains = get_domains()
    return render_template('index.html', title='Home', search_input='', site_info_input='', domains=domains)

@app.route("/search-results/")
def search_results():
    search_input = request.args.get('search_input')
    page_num = request.args.get('page_num')
    page_limit = 20
    domains = get_domains()
    results = dict()
    # search_engine = 'sqlite'
    search_engine = 'elastic'
    if search_engine == 'sqlite':
        cur = get_db().cursor()
        cur.execute("SELECT * FROM pages WHERE content LIKE ?", ['%' + search_input + '%'])
        results = cur.fetchall()
        for result in results:
            result_display = dict(result)
            match = re.search(search_input, result_display['content'], re.IGNORECASE)
            if match is not None:
                result_display['text_before'] = result_display['content'][match.span(0)[0] - 100:match.span(0)[0]]
                result_display['search_input'] = result_display['content'][match.span(0)[0]:match.span(0)[1]]
                result_display['text_after'] = result_display['content'][match.span(0)[1]:match.span(0)[1] + 100]
                results_display.append(result_display)

    elif search_engine == 'elastic':
        # search_elastic = And([Term("content", u"apple"), Term("content", "bear")]) # You need to do AND for each word in the users's query here
        # parser = QueryParser("content", ix.schema)
        # search_query = parser.parse(search_input)
        # results = searcher.search(search_query)
        es = Elasticsearch()
        res = es.search(index="pages", doc_type="page", body={
            "from" : (int(page_num) - 1) * page_limit, "size" : page_limit,
            "query": {
                "match": {
                    "content": search_input
                }
            },
            "highlight": {
                "fields": {
                    "content": {}
                }
            }
        })
        results['total_results'] = res['hits']['total']
        pagination_pages_num = results['total_results'] // page_limit
        if results['total_results'] % page_limit != 0:
            pagination_pages_num = pagination_pages_num + 1
        results['pagination_pages'] = list()
        for n in range(1, pagination_pages_num + 1):
            results['pagination_pages'].append({'num': n, 'url': '%s?search_input=%s&search_submit=Search&page_num=%s' % (request.base_url, search_input, n)})
        results['pages'] = list()
        for page in res['hits']['hits']:
            result_display = dict()
            result_display['url'] = page['_source']['url']
            result_display['text_before'] = 'test txt before'
            result_display['search_input'] = page['highlight']['content'][0]
            result_display['text_after'] = 'test txt after'
            # page['source']['content']
            results['pages'].append(result_display)

    else:
        exit(0)

    return render_template('search_results.html', title='Search Results', search_input=search_input, domains=domains, results=results, page_num = int(page_num))

@app.route("/site-info-results/")
def site_info_results():
    site_info_input = request.args.get('site_info_input')
    page_num = request.args.get('page_num')
    cur = get_db().cursor()
    cur.execute("SELECT domain FROM domains WHERE id = ?", (site_info_input,))
    results = dict()
    results['domain'] = cur.fetchone()['domain']
    cur.execute("SELECT COUNT(id) from pages WHERE domain_id = ?", (site_info_input,))
    results['num_pages'] = cur.fetchone()[0]
    page_limit = 20
    pagination_pages_num = int(results['num_pages'] / page_limit) + 1
    results['pagination_pages'] = list()
    for n in range(1, pagination_pages_num + 1):
        results['pagination_pages'].append({'num': n, 'url': '%s?site_info_input=%s&site_info_submit=Search&page_num=%s' % (request.base_url, site_info_input, n)})
    page_start = (int(page_num) - 1) * page_limit
    cur.execute("SELECT url, last_crawled FROM pages WHERE domain_id = ? LIMIT ?,?", (site_info_input, page_start, page_limit))
    results['pages'] = [dict(row) for row in cur.fetchall()]
    domains = get_domains()
    return render_template('site_info_results.html', title='Site Info Results', domains=domains, search_input='', site_info_input=int(site_info_input), results=results, page_num = int(page_num))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()