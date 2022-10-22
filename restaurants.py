import json
from flask import request,make_response
from uuid import uuid4
from dbhelpers import conn_exe_close
from apihelpers import verify_endpoints_info

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

# specific restaurant will return the restaurant with specific id given as a param
# this function will fulfill the get request
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

    
def restaurant_post():
    invalid = verify_endpoints_info(request.json,['name','address','phone_num','bio','city','email','profile_url','banner_url','password'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    token = uuid4().hex
    salt = uuid4().hex
    results = conn_exe_close('call restaurant_post(?,?,?,?,?,?,?,?,?,?,?)',
    [request.json.get('name'),request.json.get('address'),request.json.get('phone_num'),request.json.get('bio'),
    request.json.get('city'),request.json.get('email'),request.json.get('profile_url'),
    request.json.get('banner_url'),request.json.get('password'),token,salt])
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)

