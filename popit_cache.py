import popit
from pymongo import MongoClient


class BasePopitCache(object):

    def conn_wrapper(self, entity):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["ocds_hack"]
        collection = self.db[entity]
        return collection


class PopitCacheWriter(BasePopitCache):
    def __init__(self):
        self.popit_client = popit.PopitClient()

    def fetch_persons(self):
        companies = self.conn_wrapper("director")
        for company in companies.find():
            for director in company["directors"]:
                pass

    def write_cache(self, entity, data):
        collection = self.conn_wrapper(entity)
        collection.update({"id":data["id"]}, data, upsert=True)


class PopitCacheReader(BasePopitCache):
    pass