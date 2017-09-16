from flask import Flask
from flask import jsonify
from pymongo import MongoClient
import popit

app = Flask(__name__)

@app.route("/ocds/<entity>/")
def list_ocds_entity(entity):
    client = MongoClient('mongodb://localhost:27017/')
    db = client["ocds_hack"]
    collection = db[entity]

    data = []
    for i in collection.find():
        temp = i
        del temp["_id"]
        data.append(i)
     
    return jsonify({ 'results': data })

@app.route("/ocds/<entity>/<id>")
def get_ocds_entity(entity, id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client["ocds_hack"]
    collection = db[entity]

    result = collection.find_one({"id":id})
    del result["_id"]

    return jsonify({ 'result': result })

# I can use short cut but each popit entity have different action
# Also list view and single item view is different
@app.route("/organizations/")
def get_organizations():
    popit_client = popit.PopitClient()
    organizations = popit_client.get_entities("organizations")
    if "error" in organizations:
        pass
    
    pass

@app.router("/organizations/<entity_id>")
def get_organization(entity_id):
    popit_client = popit.PopitClient()
    organization = popit_client.get_entity("organizations", entity_id)
    if "error" in organization:
        pass

    pass

@app.route("/persons/")
def get_persons():
    popit_client = popit.PopitClient()
    organizations = popit_client.get_entities("persons")
    if "error" in organizations:
        pass
    
    pass

@app.router("/persons/<entity_id>")
def get_person(entity_id):
    popit_client = popit.PopitClient()
    organization = popit_client.get_entity("persons", entity_id)
    if "error" in organization:
        pass

    pass


