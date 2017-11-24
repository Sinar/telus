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
        parties = self.conn_wrapper("award")
        error_count = 0
        page = 1
        while True:
            print(page)
            persons = self.popit_client.get_entities("persons", page)

            if "error" in persons:
                print(persons["error"])
                break

            for person in persons["results"]:
                written = False
                temp = companies.find({"directors.name": {'$regex': person["name"].upper()}})
                if temp.count():
                    self.write_cache("persons", person)
                    written = True

                if not written:
                    for membership in person["memberships"]:
                        temp = parties.find({"parties.name": membership["organization"]["name"]})
                        if temp.count():
                            self.write_cache("persons", person)

            page = page + 1

    def write_cache(self, entity, data):
        collection = self.conn_wrapper(entity)
        collection.update({"id":data["id"]}, data, upsert=True)

    def fetch_cache(self, entity, data):
        collection = self.conn_wrapper(entity)
        return collection.find_one({"id": data["id"]})


if __name__ == "__main__":
    cache = PopitCacheWriter()
    cache.fetch_persons()

