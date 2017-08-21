import unittest
import app
from elasticsearch import Elasticsearch

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    # def tearDown(self):
    #     pass

    def test_index(self):
        ind = self.app.get('/')
        assert b'Will Search' in ind.data

    def test_elastic(self):
        es = Elasticsearch()
        search_input = 'manchester'
        search_from = 20
        search_size = 1
        res = es.search(index="pages", doc_type="page", body={
            "from" : search_from, "size" : search_size,
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
        return res

if __name__ == '__main__':
    unittest.main()