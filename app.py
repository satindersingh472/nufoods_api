# import flask for api
from flask import Flask
# import dbcreds to check for production mode
import dbcreds
# import client.py for client endpoints
from clients import client_login,client_logout,specific_client,add_client,client_delete
from restaurants import  restaurant_login,restaurant_logout,all_restaurants,specific_restaurant,restaurant_post,restaurant_delete
from menu import all_menu,menu_delete,menu_post

app = Flask(__name__)

# this is for the client login endpoint
@app.post('/api/client_login')
def use_client_login():
    return client_login()


# this is for the client login delete method
@app.delete('/api/client_login')
def use_client_logout():
    return client_logout()
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
# -------------------------------------------------------------------------------------------------------------------
# will login the restaurant using restaurant login module
# POST
@app.post('/api/restaurant_login')
def use_restaurant_login():
    return restaurant_login()

# will logout the restaurant
# DELETE
@app.delete('/api/restaurant_login')
def use_restaurant_logout():
    return restaurant_logout()

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

@app.post('/api/restaurant')
def use_restaurant_post():
    return restaurant_post()

@app.delete('/api/restaurant')
def use_restaurant_delete():
    return restaurant_delete()

# -----------------------------------------------------------------------------------------------------------------------
@app.get('/api/menu')
def use_all_menu():
    return all_menu()

@app.post('/api/menu')
def use_menu_post():
    return menu_post()

@app.delete('/api/menu')
def use_menu_delete():
    return menu_delete()

# ___________the end_________________

if(dbcreds.production_mode == True):
    print('Running in PRODUCTION MODE')
    import bjoern #type: ignore
    bjoern.run(app,'0.0.0.0',5001)
else:
    from flask_cors import CORS
    CORS(app)
    print('Running in TESTING MODE')
    app.run(debug=True)


