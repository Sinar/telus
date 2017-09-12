from pymongo import MongoClient
import json
import os


class CIDBProcessor(object):

    def __init__(self, uri='mongodb://localhost:27017/', datapath="./"):
        self.client = MongoClient(uri)
        self.datapath = datapath
        self.template = {

                }


class CIDBData(object):
    def __init__(self, data):
        self.data = data

    def projects(self):
        return self.data["projects"]

    @property
    def profiles(self):
        return self.data["Profil"]

    # TODO: Convert company into OCDS Org
    # TODO: Find ID from OCDS
    def ocds_vendor(self):
        data = {
            "scheme":"CIDB",
            "id": self.profiles["Nombor Pendaftaran"],
            "legalName": self.data["name"],
        }

        return data 

    # TODO: CIDB entry have multiple projects/award
    def ocds_award(self):
        data = {
                }

        return data





