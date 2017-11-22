import popit
from pymongo import MongoClient
import time


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
                name = director["name"]
                results = self.popit_client.search_entity("persons", "name", name)
                # If not zero
                if results["total"]:
                    self.write_cache("persons", results["results"][0])

    def write_cache(self, entity, data):
        collection = self.conn_wrapper(entity)
        collection.update({"id":data["id"]}, data, upsert=True)

