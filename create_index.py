from elasticsearch import Elasticsearch

class Index:
    def __init__(self):
        self.__mappings = {"mappings": {"properties": {"age": {"type": "long"},"entry": {"type": "date"},"name": {"type": "text","fields": {"keyword": {"type": "keyword","ignore_above": 256 }}},"objective": {"type": "text","fields": {"keyword": {"type": "keyword","ignore_above": 256}}},"sent_vec": {"type": "dense_vector","dims": 768}}}}
    

    def create_index(self, name):
        es = Elasticsearch(HOST = 'https://localhost', PORT = 9200)
        es.create(index= name, ignore=400, body= self.__mappings)
