# apistudy
A RESTful API case study. This service uses Flask and sqlite. It stores, retrieves, and deletes AirBnB style listings from a database.

Setup instructions:
* get `virtualenv`
* clone this repository
* `virtualenv env` in its root directory
* `. env/bin/activate` in the same place
* `pip install flask`
* `pip install flask-sqlalchemy`
* `pip install sqlalchemy-migrate`
* `./createdb.py`
* `./migratedb.py`
* `./run.py`

The file `apistudy/app/views.py` documents the endpoints available in this service. Here are some example invocations:
* `curl localhost:9100/health`
* `curl -H "Content-Type: application/json" -X POST -d '{"user": "Hamik", "title": "Great apartment in SoMa", "description": "Watch out for poo on the sidewalk, but bask in spotless luxury and the buzzing silence of laminated double-pane windows once inside.", "expiration": "2018-01-01T00:00:00", "location": {"x": -122.400917, "y": 37.781323}}' localhost:9100/api/listings` puts the given listing in the database
* `curl localhost:9100/api/listings` retrieves all listings
* `curl localhost:9100/api/listings/2` retrieves the listing with the given id
* `curl localhost:9100/api/listings?active=1` retrieves only listings that haven't expired
* `curl 'localhost:9100/api/listings?length=1&page=2'` retrieves paginated listings
* `curl -X DELETE 'localhost:9100/api/listings/2'` deletes the given listing
* `curl -X DELETE 'localhost:9100/api/listings'` deletes all listings
* `curl -H "Content-Type: application/json" -X PUT -d '{"user": "Bob", "title": "White camper van", "description": "Parked by the bridge near El Cap Meadow", "expiration": "2018-01-01T00:00:00", "location": {"x":  -119.630541, "y": 37.723773}}' localhost:9100/api/listings/1` overwrites listing 1 with the given listing
