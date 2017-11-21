import popit
from pymongo import MongoClient


class BasePopitCache(object):

    def conn_wrapper(self, entity):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["ocds_hack"]
        collection = self.db[entity]
        return collection


class PopitCacheLoader(BasePopitCache):
    def __init__(self, api_url):
        pass

    def load_cache(self):
        pass


class PopitCacheReader(BasePopitCache):
    pass