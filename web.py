from flask import Flask
from flask import jsonify
from flask import render_template
from pymongo import MongoClient
import popit

app = Flask(__name__)

def conn_wrapper(entity):
    client = MongoClient('mongodb://localhost:27017/')
    db = client["ocds_hack"]
    collection = db[entity]
    return collection

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
        return render_template("error.html", error=organizations["error"])

    return render_template("agency.html", organization=organizations["result"], contracts=contracts)

@app.router("/organizations/<entity_id>")
def get_organization(entity_id):
    popit_client = popit.PopitClient()
    organization = popit_client.get_entity("organizations", entity_id)
    if "error" in organization:
        return render_template("error.html", error=organizations["error"])

    coll = conn_wrapper("award")
    result = organizations["result"]
    contracts = []
    for contract in coll.find({"buyer.name": result["name"]}):
        company = None
        for supplier in contract["parties"]:
            if supplier["role"] == "supplier":
                company = supplier["name"]

        temp = {
            "company": company,
            "description": contraction["awards"][0]["description"],
            "procuring_agency":contract["buyer"]["name"],
            "start_date": contract["date"],
            "amount": contract.value.amount

        }
        contracts.append(temp)

    return render_template("agency.html", organization=organizations["result"], contracts=contracts)

@app.route("/persons/")
def get_persons():
    popit_client = popit.PopitClient()
    organizations = popit_client.get_entities("persons")
    if "error" in organizations:
        return render_template("error.html", error=organizations["error"])
    
    pass

@app.router("/persons/<entity_id>")
def get_person(entity_id):
    popit_client = popit.PopitClient()
    person = popit_client.get_entity("persons", entity_id)
    if "error" in organization:
        return render_template("error.html", error=organizations["error"])

    coll = conn_wrapper("award")
    result = person["result"]
    contracts = []

    for membership in result["memberships"]:
        for contract in coll.find({ "parties.name": membership["organizations"]["name"]}):
            temp = {
                "company": membership["organizations"]["name"],
                "description": contraction["awards"][0]["description"],
                "procuring_agency":contract["buyer"]["name"],
                "start_date": contract["date"],
                "amount": contract.value.amount
            }
            contracts.appennd(temp)
    
    return render_template("person.html", person=result, contracts=contracts)


