from dbhelpers import conn_exe_close 
import json
from flask import request,make_response
from apihelpers import verify_endpoints_info,add_for_patch
from uuid import uuid4

# '/api/client_login' start from here for 2 different methods post and delete 
def client_login():
    # will verify that the required params are sent or not
    invalid = verify_endpoints_info(request.json,['email','password'])
    if(invalid != None):
        # if not return the response with error 400
        return make_response(json.dumps(invalid,default=str),400)
    # if given the params will continue and generate the token for procedure 
    token = uuid4().hex
    results = conn_exe_close('call client_login(?,?,?)',
    [request.json.get('email'),request.json.get('password'),token])
    # the procedure will return the results with id and token and the tuple must be of length 1
    if(type(results) == list and len(results) == 1):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == list and len(results) != 1):
        return make_response(json.dumps('username or password is not valid',default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)


# will logout the client if the valid token is given through headers
def client_logout():
    # if header is missing will show an error
    invalid_headers = verify_endpoints_info(request.headers,['token'])
    if(invalid_headers != None):
        return make_response(json.dumps(invalid_headers,default=str),400)
    # will send the request to delete the token from the database
    results = conn_exe_close('call client_logout(?)',[request.headers.get('token')])
    if(type(results) == list and results[0]['row_count'] == 1):
        # if token deleted from database then the row count will be sent back
        # if result is a list and result[0][0] == 1 then it has deleted the token 
        return make_response(json.dumps('successfully logged out',default=str),200)
        # if token is not deleted it will send 0 length of results which
    elif(type(results) == list and results[0]['row_count'] == 0):
        return make_response(json.dumps('logout not successfull or already logged out',default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)



# ------------------------------------------------------------------------------------------------
# below section is for '/api/client'

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
        return make_response(json.dumps('client does not exists',default=str),400)
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
    if( type(results) == list and results[0]['row_count'] == 1):
        return make_response(json.dumps('client deleted successfully',default=str),200)
        # if result is an empty list then client is not deleted may be password is wrong
    elif( type(results)== list and results[0]['row_count'] == 0):
        return make_response(json.dumps('no client deleted',default=str),400)
    elif(type(results) != list):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)


#patch endpoint has been done in two steps
# if user sends password it will use client_patch_with_password function 
# other wise it use client_patch
# they both are the same but with little difference in store procedure to which the request is sent to update
# in that request the store procedure is expecting couple of extra arguments like password and salt. 

# this will work for client patch without password
def client_patch():
    # will grab the client from db to use for adding missing arguments purpose
    results = conn_exe_close('call client_get_with_token(?)',[request.headers['token']])
    # if results does not come back as expected then it will return the function
    if(type(results) != list or len(results) != 1):
        return make_response(json.dumps(results,default=str),400)
    # will send the request type of arguments, required_arguments, and results got from the previous request
    # asking for details to fullfill missing arguments
    results = add_for_patch(request.json,['email','first_name','last_name','image_url','username'],results[0])
    # we can use the original arguments from database to send them with the request 
    results = conn_exe_close('call client_patch(?,?,?,?,?,?)',
    [results['username'],results['first_name'],results['last_name'],results['email'],results['image_url'],request.headers['token']])
    # if row gets changed in any way the database will return the row_count 1 and this statement will become true
    if(type(results) == list and results[0]['row_count'] == 1):
        return make_response(json.dumps('client profile updated',default=str),200)
        # if not changed anything the following statement will become true
    elif(type(results) != list or results[0]['row_count'] == 0):
        return make_response(json.dumps('client profile not changed',default=str),400)
    else:
        # if there is any other error beyond user then this statement will be true
        return make_response(json.dumps(results,default=str),500)


# it will be called when password is sent with data 
# everything is same but just sending the request to update to a new procedure with extra parameters
def client_patch_with_password():
    # will bring the original details of client just to have original data to send with request
    # if the user does not send all the data required by the stored procedure to update the row in client table
    results = conn_exe_close('call client_get_with_token(?)',[request.headers['token']])
    # if any error occurs or the client is not present with same credentials then the function will get
    # returned with an error
    if(type(results) != list or len(results) != 1):
        return make_response(json.dumps(results,default=str),400)
# will generate a new salt just to make sure we are safe
    salt = uuid4().hex
    # now the following function will check for data sent and replace the original data with the data sent to 
    # satisfy all the arguments required by the stored procedure
    results = add_for_patch(request.json,['email','first_name','last_name','image_url','username'],results[0])
    # will send the request with original plus arguments data sent by client to the stored procedure to update the row inside the client table
    results = conn_exe_close('call client_patch_with_password(?,?,?,?,?,?,?,?)',
    [results['username'],results['first_name'],results['last_name'],results['email'],
    results['image_url'],request.json['password'],request.headers['token'],salt])
    # if update is successfull then client will get a message
    if(type(results) == list and results[0]['row_count'] == 1):
        return make_response(json.dumps('client profile updated',default=str),200)
        # if not successfull then this message will be sent
    elif(type(results) != list or results[0]['row_count'] == 0):
        return make_response(json.dumps('client profile not changed',default=str),400)
    else:
        # if error is not created by user then following statement will become true
        return make_response(json.dumps(results,default=str),500)


# it will check the header and password
def client_patch_all():
    # if token is not sent as a header it will show an error
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
        # now it will check if the password is sent as request.json
        # and call the function according to the condition
    invalid = verify_endpoints_info(request.json,['password'])
    # if password is missing invalid will return something means it is not none and 
    # condition will return the following function
    if(invalid != None):
        return client_patch()
        # else it will return the function will help change the password as well
    elif(invalid == None):
        return client_patch_with_password()
    