import json
from unittest import makeSuite
from flask import request,make_response
from uuid import uuid4
from dbhelpers import conn_exe_close
from apihelpers import add_for_patch, verify_endpoints_info,constraint_password


# will login the restaurant and return the id and token for the restaurant
def restaurant_login():
    # check if email and password are present in the request
    invalid = verify_endpoints_info(request.json, ['email','password'])
    if(invalid != None):
        # if not then return the error for missing data
        return make_response(json.dumps(invalid,default=str),400)
    # will create the token if data is present
    token = uuid4().hex
    # will make the request to database to add a token and id to the restaurant session
    results = conn_exe_close('call restaurant_login(?,?,?)',
    [request.json['email'],request.json['password'],token])
    # results will return the id and token if all goes fine
    # in a form of list
    if(type(results) == list and len(results) == 1):
        return make_response(json.dumps(results,default=str),200)
        # if something is wrong then error will get returned
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps('Invalid username or password',default=str),400)
    elif(type(results) == str):
        # if there is any other error related to user then the error will be presented to the user
        return make_response(json.dumps(results,default=str),400)
    else:
        # or if there is any server error it will show up as error 500
        return make_response(json.dumps(results,default=str),500)
    

# will delete the token sent to the database from restaurant sessions
# and return the row count which should be one if all goes well
def restaurant_logout():
    # will check for the headers if token is sent
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        # if token not sent then error will be asking for token to send
        return make_response(json.dumps(invalid_header,default=str),400)
        # if token is sent then will request the database to process it further and delete the specific token from db
    results = conn_exe_close('call restaurant_logout(?)',[request.headers.get('token')])
    # if tokenn exists and got deleted and then row count will be sent back in a form of a list
    # and appropriate message will be shown to the user
    if(type(results) == list and results[0][0] == 1):
        return make_response(json.dumps('restaurant logout successfully',default=str),200)
    elif(type(results) == list and results[0][0] == 0):
        # if not successfull then error message will get displayed
        return make_response(json.dumps('restaurant logout not successfull or already logged out',default=str),400)
    else:
        # if there is any server error it will show error 500
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
            return make_response(json.dumps(results[0],default=str),200)
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
    constraint = constraint_password(request.json['password'])
    if(constraint != None):
        return make_response(json.dumps(constraint,default=str),400)
    token = uuid4().hex
    salt = uuid4().hex
    # will call the procedure to send data to the database
    results = conn_exe_close('call restaurant_post(?,?,?,?,?,?,?,?,?,?,?)',
    [request.json['name'],request.json['address'],request.json['phone_num'],request.json['bio'],
    request.json['city'],request.json['email'],request.json.get('profile_url'),
    request.json.get('banner_url'),request.json.get('password'),token,salt])
    if(type(results) == list and len(results) >= 1):
        # if list is returned then data is stored and return back the id and token
        return make_response(json.dumps(results[0],default=str),200)
    elif(type(results) == str):
        # if not then error will show up if there is any duplicate key or constraint failed
        return make_response(json.dumps(results,default=str),400)
    else:
        # if everything is ok from user side then error will be coming from server side
        return make_response(json.dumps(results,default=str),500)


# DELETE restaurant
# this will delete the restaurant with the given token as a header and restaurant id as a data
def restaurant_delete():
    # will check for header is sent or no
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        # if not sent then error will show up with code 400
        return make_response(json.dumps(invalid_header,default=str),400)
        # will check for password if sent or not either correct or incorrect
    invalid = verify_endpoints_info(request.json,['password'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    # make a request to delete the restaurant by sending the password and header
    results = conn_exe_close('call restaurant_delete(?,?)',[request.json['password'],request.headers['token']])
    if(type(results) == list):
        # if response is list then following message is displayed
        return make_response(json.dumps('restaurant deleted successfully',default=str),200)
    elif(type(results) == list and results[0][0] == 0):
        # if response row count is 0 then no restaurant deleted
        return make_response(json.dumps('no restaurant deleted',default=str),400)
    else:
        # if server error then error 500 is shown
        return make_response(json.dumps(results,default=str),500)


def restaurant_patch():
    # will bring back the restaurant details with token
    results = conn_exe_close('call restaurant_get_with_token(?)',[request.headers['token']])
    if(type(results) != list):
        # if results are not list and length 1 then return the function
        return make_response(json.dumps(results,default=str),400)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps('sorry something went wrong,log in again can solve the issue',default=str),400)
    # if results is a list of dict with len 1 then send the required arguments to the add for patch
    # to over write the data that inside original dict that we got from before has been sent by user
    # will send the required and original results and request json to overwrite the original data recieved
    results = add_for_patch(request.json,['name','address','phone_num','bio','email','city','profile_url','banner_url'],results[0])
    # after overwrite access all the key values needed to send the request for update the row
    results = conn_exe_close('call restaurant_patch(?,?,?,?,?,?,?,?,?)',
    [results['name'],results['address'],results['phone_num'],results['bio'],results['city'],results['email'],
    results['profile_url'],results['banner_url'],request.headers['token']])
    # response will be the row count from db if it is 1 then all good 
    if(type(results) == list and results[0]['row_count'] == 1):
        return make_response(json.dumps('restaurant profile updated',default=str),200)
    elif(type(results) != list or results[0]['row_count'] != 1):
        # if row count is not 1 or something else then error
        return make_response(json.dumps('restaurant profile not updated',default=str),400)
    else:
        # true if server error
        return make_response(json.dumps(results,default=str),500)  
    

def restaurant_patch_with_password():
        # will bring back the restaurant details with token
    results = conn_exe_close('call restaurant_get_with_token(?)',[request.headers['token']])
    if(type(results) != list):
        # if results are not list and length 1 then return the function
        return make_response(json.dumps(results,default=str),400)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps('sorry something went wrong,log in again can solve the issue',default=str),400)
    # if results is a list of dict with len 1 then send the required arguments to the add for patch
    # to over write the data that inside original dict that we got from before has been sent by user
    # will send the required and original results and request json to overwrite the original data recieved
    results = add_for_patch(request.json,['name','address','phone_num','bio','email','city','profile_url','banner_url'],results[0])
    # this function is just checking token as a header and password
    # because password update has a diff stored procedure
    # if password is sent then password will be sent along with request by over writing other data arguments from original data
    # to send the password we will just grab from json request and send it along with the request and send a new salt as well
    salt = uuid4().hex
    # now send the request with overwritten data and new password and salt
    results = conn_exe_close('call restaurant_patch_with_password(?,?,?,?,?,?,?,?,?,?,?)',
    [results['name'],results['address'],results['phone_num'],results['bio'],results['city'],results['email'],
    results['profile_url'],results['banner_url'],request.json['password'],salt,request.headers['token']])
    # response will be the row count from db if it is 1 then all good 
    if(type(results) == list and results[0]['row_count'] == 1):
        return make_response(json.dumps('restaurant profile updated',default=str),200)
    elif(type(results) != list or results[0]['row_count'] != 1):
        # if row count is not 1 or something else then error
        return make_response(json.dumps('restaurant profile not updated',default=str),400)
    else:
        # true if server error
        return make_response(json.dumps(results,default=str),500)  
    



# this function is just checking that is token is sent as header 
# if not token is not sent then error
# it is also checking if the password is sent or no
# if not then run the function that can update data without password
# if yes then run the function that can update the password and salt too
def restaurant_patch_all():
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
    invalid = verify_endpoints_info(request.json,['password'])
    if(invalid != None):
        return restaurant_patch()
    elif(invalid == None):
        constraint = constraint_password(json.dumps(constraint,default=str),400)
        return restaurant_patch_with_password()