from processor import DocumentProcessor
import uuid


class CIDBProcessor(DocumentProcessor):
    def __init__(self):
        super().__init__("data/cidb")

    def process_documents(self):
        for item in self.read_jsonl():
            parser = CIDBParser(item)

            seller = parser.ocds_party
            self.store_record("seller", seller)
            for project in parser.projects:
                award = parser.ocds_award(project)
                self.store_record("award", award)


class CIDBParser(object):
    def __init__(self, data):
        self.data = data

    @property
    def projects(self):
        return self.data["projects"]

    @property
    def profiles(self):
        return self.data["Profil"]

    @property
    def ocds_party(self):
        data = {
            "id": self.profiles["Nombor Pendaftaran"],
            "name": self.data["name"],
            "role": "supplier" # CIDB is all contractors, they supply service
        }

        # Each CIDB record is about 1 party. 1 contractor. 
        return data 

    # CIDB entry have multiple projects/award
    # So instead of have a list awards, we convert project into record
    # 
    def ocds_award(self, data):
        amount = data["value"]
        amount = amount.replace(",", "")
        data = {
            "id": uuid.uuid4().hex,
            "description": data["project"], # Oops this is not necessary in english
            "status": "complete", # CIDB Record is about completed project mostly
            "date": data["dates"],
            "value": {
                "amount": float(amount),
                "currency": "MYR"
            }
        }

        return data








