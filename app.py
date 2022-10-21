# import flask for api
from flask import Flask
# import dbcreds to check for production mode
import dbcreds
# import client.py for client endpoints
from clients import specific_client,add_client,client_delete
from restaurants import all_restaurants, specific_restaurant
from menu import all_menu

app = Flask(__name__)

# ------------------------------------------------------------------------------------------------------------------
# client section starts from here
# get request for all clients will get details about specific client with id
# it will use the functon from clients file 
@app.get('/api/client')
def use_specific_client():
    return specific_client()

# post client will add a new client and suppose to return the id and token
# will use the add client function from clients.py
@app.post('/api/client')
def use_add_client():
    return add_client()

@app.delete('/api/client')
def use_client_delete():
    return client_delete()


# ---------------------------------------------------------------------------------------------------------------------
# will use all restaurants function and return all the restaurants no id is required
@app.get('/api/restaurants')
def use_all_restaurants():
    return all_restaurants()

# ----------------------------------------------------------------------------------------------------------------------
# use specific restaurant function from restaurants.py
# will get information about single restaurant with given id
@app.get('/api/restaurant')
def use_specific_restaurant():
    return specific_restaurant()

# -----------------------------------------------------------------------------------------------------------------------
@app.get('/api/menu')
def use_all_menu():
    return all_menu()

if(dbcreds.production_mode == True):
    print('Running in PRODUCTION MODE')
    import bjoern #type: ignore
    bjoern.run(app,'0.0.0.0',5001)
else:
    from flask_cors import CORS
    CORS(app)
    print('Running in TESTING MODE')
    app.run(debug=True)


