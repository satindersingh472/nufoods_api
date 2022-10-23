import json
from unittest import makeSuite
from flask import request,make_response
from uuid import uuid4
from dbhelpers import conn_exe_close
from apihelpers import verify_endpoints_info

def restaurant_login():
    invalid = verify_endpoints_info(request.json, ['email','password'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    token = uuid4().hex
    results = conn_exe_close('call restaurant_login(?,?,?)',
    [request.json.get('email'),request.json.get('password'),token])
    if(type(results) == list and len(results) == 1):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps('Invalid username or password',default=str),400)
    elif(type(results) == str):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)
    

def restaurant_logout():
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
    results = conn_exe_close('call restaurant_logout(?)',[request.headers.get('token')])
    if(type(results) == list and results[0][0] == 1):
        return make_response(json.dumps('restaurant logout successfully',default=str),200)
    elif(type(results) == list and results[0][0] == 0):
        return make_response(json.dumps('restaurant logout not successfull or already logged out',default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)



# -----------------------------------------------------------------------------------------------------------------------------------------
# all restaurants will fulfill the get request and will get all the restaurants without any id given
def all_restaurants():
    results = conn_exe_close('call all_restaurants()',[])
    if(type(results) == list and len(results) >= 1):
            return make_response(json.dumps(results,default=str),200)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps('sorry, no restaurants available',default=str),200)
    elif(type(results) == str):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)


# ------------------------------------------------------------------------------------------------------------------------------------------
# specific restaurant will return the restaurant with specific id given as a param
# this function will fulfill the get request
# GET request
def specific_restaurant():
    invalid = verify_endpoints_info(request.args,['restaurant_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = conn_exe_close('call specific_restaurant(?)',[request.args.get('restaurant_id')])
    if(type(results) == list):
            return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)

# POST Request for client
# this will work for post restaurant and return the restaurant id and token back
def restaurant_post():
    # will verify if every argument is send as data 
    invalid = verify_endpoints_info(request.json,['name','address','phone_num','bio','city','email','profile_url','banner_url','password'])
    if(invalid != None):
        # if not then return the error
        return make_response(json.dumps(invalid,default=str),400)
    # if everything is sent will grab a token and salt for authentication purposes
    token = uuid4().hex
    salt = uuid4().hex
    # will call the procedure to send data to the database
    results = conn_exe_close('call restaurant_post(?,?,?,?,?,?,?,?,?,?,?)',
    [request.json.get('name'),request.json.get('address'),request.json.get('phone_num'),request.json.get('bio'),
    request.json.get('city'),request.json.get('email'),request.json.get('profile_url'),
    request.json.get('banner_url'),request.json.get('password'),token,salt])
    if(type(results) == list):
        # if list is returned then data is stored and return back the id and token
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        # if not then error will show up if there is any duplicate key or constraint failed
        return make_response(json.dumps(results,default=str),400)
    else:
        # if everything is ok from user side then error will be coming from server side
        return make_response(json.dumps(results,default=str),500)


# DELETE restaurant
# this will delete the restaurant with the given token as a header and restaurant id as a data
def restaurant_delete():
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
    invalid = verify_endpoints_info(request.json,['password'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = conn_exe_close('call restaurant_delete(?,?)',[request.json.get('password'),request.headers.get('token')])
    if(type(results) == list and results[0][0] == 1):
        return make_response(json.dumps('restaurant deleted successfully',default=str),200)
    elif(type(results) == list and results[0][0] == 0):
        return make_response(json.dumps('no restaurant deleted',default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)