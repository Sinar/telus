# telus
Joined Up Data transparency project for PEPs, OCDS &amp; Beneficial Ownership

API endpoints

* /releases
* /records
* /organizations

* /search/records
* /search/organizations
* /search/persons

# Install requirements
```
pip install -r requirements.txt
```

# To run
```
$ export FLASK_APP=web.py
$ export FLASK_DEBUG=1
$ flask run
```

# To load data
```
$ python data_loader.py
```
