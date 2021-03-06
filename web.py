from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from pymongo import MongoClient
import popit
import re

app = Flask(__name__)


def conn_wrapper(entity):
    client = MongoClient('mongodb://localhost:27017/')
    db = client["ocds_hack"]
    collection = db[entity]
    return collection


@app.route("/")
def main_page():
    return redirect("/contracts/")


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

    return render_template("agency.html", organization=organizations["results"], contracts=contracts)


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


@app.route("/persons/")
def get_persons():
    # Because we already store the cache
    persons = conn_wrapper("persons")

    result = []

    # TODO: What information we need in the list template
    for person in persons.find():
        temp = {}
        companies = conn_wrapper("director")
        company = companies.find_one({"directors.name": {'$regex':person["name"].upper()}})
        if company:
            temp["id"] = person["id"]
            temp["name"] =  person["name"]
            temp["company"] = company["name"]
            result.append(temp)

    return render_template("persons.html", persons=result)


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
    award = None
    organization = None

    for party in contract["parties"]:
        if party["role"] == "supplier":
            supplier = party
            break

    conflict = []

    result = popit_client.search_entity("organizations", "name", supplier["name"])

    director_coll = conn_wrapper("director")

    award = contract["award"][0]

    company = director_coll.find_one({"name": supplier["name"]})
    directors = company["directors"]
    persons_coll = conn_wrapper("persons")

    processed_director = []

    for director in directors:
        name = director["name"]
        person = persons_coll.find_one({"name":{"$regex": re.compile(name, re.IGNORECASE)}})
        print(person)
        dir_temp = {
            "name": name,
            "shares": director["shares"],
            "year_of_experience": director["year_of_experience"],
        }
        if person:
            for membership in person["memberships"]:
                temp = {}
                temp["name"] = person["name"]
                temp["person_id"] = person["id"]
                temp["company"] = supplier["name"]
                temp["agency"] = membership["organization"]["name"]
                temp["official_post"] = membership["label"]
                conflict.append(temp)
            dir_temp["person_id"] = person["id"]
        else:
            dir_temp["person_id"] = None
        processed_director.append(dir_temp)

    return render_template("contract.html", organization=supplier, conflict=conflict, contract=award,
                           directors=processed_director)


@app.route("/contracts/")
def get_contracts():
    coll = conn_wrapper("award")
    contracts = coll.find()

    # This is guarantee to be conflicting(Mostly)
    person_coll = conn_wrapper("persons")
    director_coll = conn_wrapper("director")
    results = []

    for person in person_coll.find():
        company = director_coll.find_one({"directors.name": {'$regex': person["name"].upper()}})
        contracts = coll.find({"parties.name": company["name"]})
        for contract in contracts:
            temp = {}
            award = contract["award"]

            # This is only awarded
            if award:
                award_value = award[0]["value"]["amount"]
                award_date = award[0]["date"]
                award_desc = award[0]["description"]
            else:
                # Should not happen, it usually means bad data
                award_value = None
                award_date = None
                award_desc = None

            temp["director"] = person["name"]
            temp["value"] = award_value
            temp["description"] = award_desc
            temp["date"] = award_date
            temp["company"] = company["name"]

            temp["contract_id"] = contract["id"]
            results.append(temp)

    return render_template("contracts.html", contracts=results)


