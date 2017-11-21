import requests

# TODO: Fork this into own project
class PopitClient(object):
    cache = {}

    def __init__(self, url="https://api.popit.sinarproject.org", language="en"):
        self.url = url
        self.language = language
        self.entities_pattern = "{url}/{language}/{entity}/{entity_id}/"
        self.entity_pattern = "{url}/{language}/{entity}/{entity_id}/"
        self.search_pattern = "{url}/{language}/search/{entity}/"
        
    def search_organization(self, name):
        url = self.search_pattern.format(url=self.url, language=self.language, entity="organizations")
        search_params = "name:{name}".format(name=name)
        response = self.request_wrapper(url, params=search_params) 
        return response

    def search_entity(self, entity, key, value):
        url = self.search_pattern.format(url=self.url, language=self.language, entity=entity)
        search_params = "{key}:{value}".format(key=key, value=value)
        response = self.request_wrapper(url, params=search_params) 
        return response

    def get_entities(self, entity, page=None):
        url = self.entities_pattern.format(url=self.url, language=self.langauge, entity=entity)
        if page:
            response = self.request_wrapper(url, params={"page": page})
        else:
            response = self.request_wrapper(url)
        return response
        
    def get_entity(self, entity, entity_id):
        url = self.entity_pattern.format(url=self.url, language=self.language, entity=entity, entity_id=entity_id)
        response = self.request_wrapper(url)
        return response
        
    def request_wrapper(self, url, params={}):
        
        r = requests.get(url, params=params)
        if r.status_code == 200:
            return r.json()
        
        return { "error": r.content, "status_code": r.status_code }



