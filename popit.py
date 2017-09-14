import requests

# TODO: Fork this into own project
class PopitClient(object):
    def __init__(self, url="https://api.popit.sinarproject.org", language="en"):
        self.url = url
        self.language = language
        self.entity_pattern = "{url}/{language}/{entity}/{entity_id}/"
        self.search_pattern = "{url}/{language}/search/{entity}/"
        
    def search_organization(self, name):
        url = self.search_pattern.format(url=self.url, language=self.language, entity="organizations")
        search_params = "name:{name}".format(name=name)
        r = requests.get(url, params={"q":search_params})
        if r.status_code == 200:
            return r.json()

        return { "error": r.content, "status_code": r.status_code }
