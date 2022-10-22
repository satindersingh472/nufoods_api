from dbhelpers import conn_exe_close 
import json
from flask import request,make_response
from apihelpers import verify_endpoints_info
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
    results = conn_exe_close('call specific_client(?)',[request.args.get('client_id')])
    if(type(results) == list and len(results) == 1):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps('0 results matched your input',default=Str),400)
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
    salt = uuid4().hex
    # token will be sent along with other arguments to run the store procedure
    results = conn_exe_close('call add_client(?,?,?,?,?,?,?,?)',
    [request.json.get('username'),request.json.get('first_name'),request.json.get('last_name'),request.json.get('email'),
    request.json.get('image_url'),request.json.get('password'),token,salt])
    # the result returning back will be a list of one tuple and with client id and token 
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
        # if not then the str with error will show up with response code 400
    elif(type(results) == str):
        return make_response(json.dumps(results,default=str),400)
        # if something goes wrong with server error 500 will show up
    else:
        return make_response(json.dumps(results,default=str),500)


# this will delete the client and return the appropriate response back 
def client_delete():
    # check if the header is included with the api request
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        # if header is missing then this statement is true and return the error with code 400
        return make_response(json.dumps(invalid_header,default=str),400)
        # no will check for password if entered
    invalid = verify_endpoints_info(request.json,['password'])
    if(invalid != None):
        # if password not sent then error will show up with code 400
        return make_response(json.dumps(invalid,default=str),400)
        # if everything is included then it will run the stored procedure
    results = conn_exe_close('call client_delete(?,?)',[request.json.get('password'),request.headers.get('token')])
    # if results is in list form and it sends 1 back means number of rows updated is 1
    # then this means that client is deleted successfully
    if( type(results) == list and results[0][0] == 1):
        return make_response(json.dumps('Client deleted successfully',default=str),200)
        # if result is an empty list then client is not deleted may be password is wrong
    elif( type(results)== list and results[0][0] == 0):
        return make_response(json.dumps('No client deleted',default=str),400)
    elif(type(results) != list):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)