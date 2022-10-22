import json
from flask import request,make_response
import json
from apihelpers import get_display_results,verify_endpoints_info
from uuid import uuid4


# specific client will return the client with the provided input id
def specific_client():
    # check for client id is given or no
    invalid = verify_endpoints_info(request.args,['client_id'])
    if(invalid != None):
        # if not sent as a param then it will show an error
        return make_response(json.dumps(invalid,default=str),400)
        # is sent then it will go further and call the function to add client wit given all 
        # the data inside params
    results = get_display_results('call specific_client(?)',[request.args.get('client_id')])
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)

# add client will add the new client to the database and return the id of newly inserted client
def add_client():
    # will check if all the required params are sent
    invalid = verify_endpoints_info(request.json,['username','first_name','last_name','email','image_url','password'])
    if(invalid != None):
        # if not then it will ask for to send
        return make_response(json.dumps(invalid,default=str),400)
        # if sent then it will generate a token and send it along with
        # other data params to the stored procedure
    token = uuid4().hex
    results = get_display_results('call add_client(?,?,?,?,?,?,?)',
    [request.json.get('username'),request.json.get('first_name'),request.json.get('last_name'),request.json.get('email'),
    request.json.get('image_url'),request.json.get('password'),token])
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)

def token_valid():
    invalid = verify_endpoints_info(request.headers,['token'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = get_display_results('call client_token_id(?)',[request.headers.get('token')])
    return results


def client_delete():
    id = token_valid()
    if(type(id) == list and type(id[0][0]) == int and id[0][1] == 1):
        invalid = verify_endpoints_info(request.json,['password'])
        if(invalid != None):
            return make_response(json.dumps(invalid,default=str),400)
        results = get_display_results('call client_delete(?,?)',
        [id[0][0],request.json.get('password')])
        if( type(results) == list and results[0][0] == 1):
            results_json = make_response(json.dumps('Client deleted successfully',default=str),200)
            return results_json
        elif( type(results)== list and results[0][0] == 0):
            return make_response(json.dumps('No client deleted',default=str),400)
        elif(type(results) != list):
            return make_response(json.dumps(results,default=str),400)
        else:
            return make_response(json.dumps(results,default=str),500)
    elif(type(id) == list and id[0][0] != int and id[0][1] == 0):
        return make_response(json.dumps('No user exists with these credentials',default=str),400)
    elif(type(id) != list or type(id) == str):
        return id
    else:
        return make_response(json.dumps('Sorry, something went wrong',default=str),500)