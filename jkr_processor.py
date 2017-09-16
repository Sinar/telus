from processor import DocumentProcessor
import popit
import datetime
import uuid
from pymongo import MongoClient
import yaml

config = yaml.load(open("config.yaml"))

class JKRProcessor(DocumentProcessor):
    def __init__(self):
        super().__init__("data/jkr")

    def process_documents(self):
        for item in self.read_jsonl():
            parser = JKRParser(item)
            self.store_record("seller", parser.ocds_seller())
            self.store_record("buyer", parser.ocds_buyer())
            self.store_record("award", parser.ocds_award())


# Each of the data parser(?) is different. 
# Different data source provide different type of information 
class JKRParser(object):
    '''
            Sample data
    
            {
                'contractor': 'Pertama Makmur Sdn Bhd', 
                'notes': '', 
                'construction_end': '11/12/2008', 
                'title': 'Cadanga menaiktaraf jalan dari Pohon Baru (Simpang Tamu) ke Pancur Hitam, Wilayah Persekutuan, Labuan.', 
                'construction_start': '15/12/2006', 
                'cost': 'RM 52,800,000.00', 
                'offering_office': 'CAWANGAN JALAN IBU PEJABAT JKR MALAYSIA,JALAN SULTAN SALAHUDDIN,50582 KUALA LUMPUR.', 
                'source_agency': 'jkr', 
                'advertise_date': '05/01/2006', 
                'source_url': 'https://www.jkr.gov.my/ckub/b_admin/t_resultdtl.asp?No_Proj=15137', 
                'id': '15137'
           } 
    '''
    def __init__(self, data, uri='mongodb://localhost:27017/', db="ocds_hack"):
        self.data = data
        self.popit_client = popit.PopitClient()
        self.client = MongoClient(uri)
        self.db = self.client[db]
    
    def ocds_seller(self):
        contractor = self.data["contractor"]
        results = self.search_mongo("seller", contractor)

        if results.count() > 0:
            # Return first result
            return results[0]
        if config["enable_popit"]:
            results = self.search_popit(contractor)
        else:
            results = []
        data = {
            "name": contractor,
            "role": "supplier",
        }
        if results:
            # Assume first result in POC
            result = results[0]
            data["id"] = result["id"]
        else:
            data["id"] = uuid.uuid4().hex

        return data

    def search_mongo(self, coll_name, value):
        collection = self.db["seller"]
        results = collection.find({"name":value})
        return results

    def ocds_buyer(self):
        # Always offering_office
        offering_office = self.data["offering_office"]
        results = self.search_mongo("buyer", offering_office)
        if results.count() > 0:
            return results[0]
        
        if config["enable_popit"]: 
            results = self.search_popit(offering_office)
        else:
            results = []
        data = {
            "name": offering_office,
            "role": "buyer",
        }
        if results:
            # Assume first result in POC
            result = results[0]
            data["id"] = result["id"]
        else:
            data["id"] = uuid.uuid4().hex

        return data

    def ocds_award(self):
        # Assume each project is unique
        money = self.data["cost"]
        if money:
            value = self.parse_money(money)
        else:
            value = {}
        data = {
            "id": uuid.uuid4().hex,
            "description": self.data["title"],
            "status": self.get_status(),
            "date": self.data["construction_start"],
            "value": value
        }

        return data

    def parse_money(self, value):
        currency, amount = value.split(" ")
        amount = amount.replace(",","")
        amount = float(amount)
        return { "currency":currency, "amount":amount }

    def search_popit(self, name):
        results = self.popit_client.search_organization(name)
        return results["results"]

    # Because project data have future date
    def get_status(self):
        if not self.data["construction_start"]:
            return ''
        start_date = datetime.datetime.strptime(self.data["construction_start"], "%d/%m/%Y")
        today = datetime.date.today()

        if today > start_date.date():
            return "active"

        elif today < start_date.date():
            return "planning"

        end_date = datetime.datetime.strptime(self.data["construction_end"], "%d/%m/%Y")
        if today > end_date.date():
            return "complete" #Assume complete. We don't know for sure actually 

    def ocds_award_record(self):
        ocis = uuid.uuid4().hex

        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        data = {
            "ocid": ocid,
            "id": ocid + "01-award",
            "date": now,
            "language":"en",
            "tag":[ "award" ], 
            "initiationType":"Tender", # We assume that CIDB initiated by tender. Mostly true
            "parties": [ self.party ],
            "buyer": [], # CIDB record don't show buyer information
            "award":[
                self.ocds_award(data),
            ]
        }
        
        return data


