import json
from flask import request,make_response
import json
from apihelpers import get_display_results,verify_endpoints_info
from uuid import uuid4


# specific client will return the client with the provided input id
def specific_client():
    invalid = verify_endpoints_info(request.args,['client_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = get_display_results('call specific_client(?)',[request.args.get('client_id')])
    results_json = make_response(json.dumps(results,default=str),200)
    return results_json

# add client will add the new client to the database and return the id of newly inserted client
def add_client():
    invalid = verify_endpoints_info(request.json,['username','first_name','last_name','email','image_url','password'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    token = uuid4().hex
    results = get_display_results('call add_client(?,?,?,?,?,?,?)',
    [request.json.get('username'),request.json.get('first_name'),request.json.get('last_name'),request.json.get('email'),
    request.json.get('image_url'),request.json.get('password'),token])
    results_json = make_response(json.dumps(results,default=str),200)
    return results_json

def token_valid():
    invalid = verify_endpoints_info(request.json,['token'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = get_display_results('call client_token_id(?)',[request.json.get('token')])
    return results[0][0]


def client_delete():
    id = token_valid()
    invalid = verify_endpoints_info(request.json,['password'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = get_display_results('call client_delete(?,?)',
    [id,request.json.get('password')])
    if(results[0][0] == 1):
        results_json = make_response(json.dumps('Client deleted successfully',default=str),200)
        return results_json
    elif(results[0][0] == 0):
        return make_response(json.dumps('No client deleted',default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)