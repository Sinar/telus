from pymongo import MongoClient
import json
import os
import uuid
import datetime


class CIDBProcessor(object):

    def __init__(self, uri='mongodb://localhost:27017/', datapath="./data/cidb", db="cidb"):
        self.client = MongoClient(uri)
        self.datapath = datapath
        self.db = self.client[db]

    def read_jsonl(self):
        for item in os.listdir(self.datapath):
            # TODO: Might need a path.join here
            f = open(os.path.join(self.datapath,item))
            for entry in f:
                data = json.loads(entry)
                cidb = CIDBData(data)
                yield cidb

    def store_result(self):
        for item in self.read_jsonl():
            vendor_col = db["vendor"]
            record_col = db["record"]
            award_col = db["award"]
            vendor_col.insert_one(item.ocds_parties)
            for record in item.ocds_record():
                record_col.insert_one(record)

            for project in item.ocds_projects():
                award_col.insert_one(project)

            
# TODO: try to see if we can fit in tender
# TODO: CIDB project is mostly about completed. 
class CIDBData(object):
    def __init__(self, data):
        self.data = data

    @property
    def projects(self):
        return self.data["projects"]

    @property
    def profiles(self):
        return self.data["Profil"]

    # We don't have SSM in OCDB record, 
    # TODO: Look at open corporates list
    @property
    def ocds_vendor_identifier(self):
        data = {
            "scheme":"CIDB",
            "id": self.profiles["Nombor Pendaftaran"],
            "legalName": self.data["name"],
        }

        return data 

    @property
    def ocds_parties(self):
        data = {
            "id": self.profiles["Nombor Pendaftaran"],
            "name": self.data["name"],
            "identifier": self.ocds_vendor_identifier,
            "role": "supplier" # CIDB is all contractors, they supply service
        }

        # Each CIDB record is about 1 party. 1 contractor. 
        return [ data ]

    # CIDB entry have multiple projects/award
    # So instead of have a list awards, we convert project into record
    # 
    def ocds_award(self, data):
        amount = data["value"]
        amount = amount.replace(",", "")
        data = {
            "id": uuid.uuid4(),
            "description": data["project"], # Oops this is not necessary in english
            "status": "complete", # CIDB Record is about completed project mostly
            "date": data["dates"],
            "value": {
                "amount": float(amount)
                "currency": "MYR"
            }
        }

        return data

    def ocds_awards(self):
        for project in projects:
            yield self.ocds_award(project)

    def ocds_record(self):
        parties = self.ocds_parties

        # Each project 1 record
        for project in self.projects:
            award = self.ocds_award(project)
            now = datetime.datetime.now()
            data = {
                "packages":[], # TODO: Fix this
                "publishedDate": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "publisher": {}, # Create us as publisher
                "records":[
                    {
                        "compiledRelease": {
                            "award": [
                                award
                            ],
                            "buyer": {}, # TODO: We don't have that
                            "date": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "id": uuid.uuid4().hex,
                            "initiationType": "tender", 
                            "language": "en",
                            "ocid": uuid.uuid4().hex, 
                            "parties": parties,
                            "tag": [ "compiled" ], 
                            "tender": [] # We have no tender information
                        },
                        "ocid": uuid.uuid4().hex, 
                        "releases": [] # TODO look at the value
                    }
                ],


            }
            yield data




