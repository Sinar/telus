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
     
    return jsonify({'results': data})


@app.route("/ocds/<entity>/<entity_id>")
def get_ocds_entity(entity, entity_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client["ocds_hack"]
    collection = db[entity]

    result = collection.find_one({"id": entity_id})
    del result["_id"]

    return jsonify({'result': result})


# I can use short cut but each popit entity have different action
# Also list view and single item view is different
@app.route("/organizations/")
def get_organizations():
    popit_client = popit.PopitClient()
    organizations = popit_client.get_entities("organizations")
    if "error" in organizations:
        return render_template("error.html", error=organizations["error"])

    contracts = None

    return render_template("agency.html", organization=organizations["result"], contracts=contracts)


@app.route("/organizations/<entity_id>")
def get_organization(entity_id):
    popit_client = popit.PopitClient()
    organizations = popit_client.get_entity("organizations", entity_id)
    if "error" in organizations:
        return render_template("error.html", error=organizations["error"])

    memberships = []

    for membership in organizations.memberships:
        email = ""
        phone = ""
        for contact_details in membership["contact_details"]:
            if contact_details["type"] == "phone":
                phone = phone

                continue
            if contact_details["type"] == "email":
                email = email
                continue
        
        if membership.post:
            post_label = membership["post"]["label"]
        else:
            post_label = ""

        temp = {
            "person_name": membership["person"]["name"],
            "post_label": post_label,
            "start_date": membership["start_date"],
            "end_date": membership["end_date"],
            "phone": phone,
            "email": email,

        }
        memberships.append(temp)

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
            "description": contract["awards"][0]["description"],
            "procuring_agency": contract["buyer"]["name"],
            "start_date": contract["date"],
            "amount": contract.value.amount

        }
        contracts.append(temp)

    return render_template("agency.html", organization=organizations["result"], contracts=contracts, 
                           memberships=memberships)

# TODO: How does this work
# TODO: Why
@app.route("/persons/")
def get_persons():
    popit_client = popit.PopitClient()
    persons = popit_client.get_entities("persons")
    if "error" in persons:
        return render_template("error.html", error=persons["error"])

    coll = conn_wrapper("award")

    result = persons["result"]

    output = []
    for person in result:

        for membership in person["memberships"]:
            for contract in coll.find({"parties.name": membership["organization"]["name"]}):
                temp = {
                    "company": membership["organization"]["name"],
                    "description": contract["awards"][0]["description"],
                    "procuring_agency": contract["buyer"]["name"],
                    "start_date": contract["date"],
                    "amount": contract["value"]["amount"]
                }
                output.append(temp)

    return render_template("persons.html", persons=output)


@app.route("/persons/<entity_id>")
def get_person(entity_id):
    popit_client = popit.PopitClient()
    person = popit_client.get_entity("persons", entity_id)
    if "error" in person:
        return render_template("error.html", error=person["error"])

    coll = conn_wrapper("award")
    result = person["result"]
    contracts = []
    check = set()
    for membership in result["memberships"]:
        for contract in coll.find({"parties.name": membership["organization"]["name"]}):
            temp = {
                "company": membership["organization"]["name"],
                "description": contract["awards"][0]["description"],
                "procuring_agency": contract["buyer"]["name"],
                "start_date": contract["date"],
                "amount": contract["value"]["amount"]
            }
            check.add(membership["organizations"]["name"])
            contracts.append(temp)

    dir_coll = conn_wrapper("director")
    
    for entry in dir_coll.find({"directors.name": {'$regex': result["name"].upper()}}):
        
        if entry["name"] not in check:
            for contract in coll.find({"parties.name": entry["name"]}):
                print(contract)
                if contract["buyer"]:
                    buyer = contract["buyer"]["name"]
                else:
                    buyer = ""
                
                if contract["award"][0]["value"]:
                    amount = contract["award"][0]["value"]["amount"]
                else:
                    amount = None

                temp = {
                    "company": entry["name"],
                    "description": contract["award"][0]["description"],
                    "procuring_agency": buyer,
                    "start_date": contract["award"][0]["date"],
                    "amount": amount
                }
                check.add(entry["name"])
                contracts.append(temp)
    
    return render_template("person.html", person=result, contracts=contracts)


@app.route("/contracts/<entity_id>")
def get_contract(entity_id):
    popit_client = popit.PopitClient()

    coll = conn_wrapper("award")
    contract = coll.find_one({"id": entity_id})
    
    supplier = None
    for party in contract["parties"]:
        if party["role"] == "supplier":
            supplier = party
            break

    conflict = []

    result = popit_client.search_entity("organizations", "name", supplier["name"])

    # TODO: modify template
    # TODO: Maybe add new table, 
    
    if result["results"]:
        organization = result["results"][0]
        director_coll = conn_wrapper("director")
        # There shall only be one
        company = director_coll.find_one({"name": supplier["name"]})
        directors = company["directors"]

        for membership in organization["memberships"]:
            if membership["person"]["name"] in directors:
                temp = {
                    "name": membership["person"]["name"],
                    "company": supplier["name"],
                    "official_post": membership["label"],
                }
                
                conflict.append(temp)

    else:
        organization = {}

    return render_template("contracts.html", organization=organization, conflict=conflict)


