import json
from dbhelpers import conn_exe_close
from flask import request,make_response
from apihelpers import verify_endpoints_info

def order_restaurant_get():
    # will request the data only with token and bring back all the orders regardless 
    # of confirm or complete
    results = conn_exe_close('call order_restaurant_get(?)',[request.headers['token']])
    # list of results means a response is okay
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        # str of results means problem with user input
        return make_response(json.dumps(results,default=str),400)
    else:
        # else if something goes wrong even after user sends correct info then it is server error
        return make_response(json.dumps(results,default=str),500)


def order_restaurant_get_confirmed():
    # check for user input for is confirmed argument 
    # if true it will store 1 in data_one variable which means true for database
    # if false then it will send 0 which means false for database
    if(request.args['is_confirmed'] in ['true','True']):
        data_one = 1
    elif(request.args['is_confirmed'] in ['false','False']):
        data_one = 0
    results = conn_exe_close('call order_restaurant_get_confirmed(?,?)',[request.headers['token'],data_one])
    # will send request and expect a list in return 
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        # str of results means problem with user input
        return make_response(json.dumps(results,default=str),400)
    else:
        # else if something goes wrong even after user sends correct info then it is server error
        return make_response(json.dumps(results,default=str),500)

def order_restaurant_get_completed():
    # check for user input for is complete argument 
    # if true it will store 1 in data_one variable which means true for database
    # if false then it will send 0 which means false for database
    if(request.args['is_completed'] in ['true','True']):
        data_one = 1
    elif(request.args['is_completed'] in ['false','False']):
        data_one = 0
    results = conn_exe_close('call order_restaurant_get_completed(?,?)',[request.headers['token'],data_one])
    # will send request and expect a list in return 
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        # str of results means problem with user input
        return make_response(json.dumps(results,default=str),400)
    else:
        # else if something goes wrong even after user sends correct info then it is server error
        return make_response(json.dumps(results,default=str),500)

def order_restaurant_get_both():
    # will save json arguments in variables for check purpose
    is_completed = request.args['is_completed']
    is_confirmed = request.args['is_confirmed']
    # check if confirm is true or false and send that to the database either 0 or 1 based on bool
    if(is_confirmed in ['true','True']):
        data_one = 1
    elif(is_confirmed in ['false','False']):
        data_one = 0
        # checkk if c
    if(is_completed in ['true','True']):
        data_two = 1
    elif(is_completed in ['false','False']):
        data_two = 0
    results = conn_exe_close('call order_restaurant_get_both(?,?,?)',
    [request.headers['token'],data_one,data_two])
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        # str of results means problem with user input
        return make_response(json.dumps(results,default=str),400)
    else:
        # else if something goes wrong even after user sends correct info then it is server error
        return make_response(json.dumps(results,default=str),500)



def restaurant_get():
    # will check for header sent if not then error will show up
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
        # store the arguments json with in variables for easy checking
    is_confirmed = request.args.get('is_confirmed')
    is_completed = request.args.get('is_completed')
    # if no data argument is sent then this statement will be true and execute the function
    if(is_confirmed == None and is_completed == None):
        return order_restaurant_get()
    #if both is completed and is confirmed are sent then the following statement become true and execute the function 
    elif(is_confirmed != None and is_completed != None):
        return order_restaurant_get_both()   
        # if is confirm is sent then the following statement will become true and execute the function
    elif(is_confirmed != None and is_completed == None):
        return order_restaurant_get_confirmed()
        # if is completed is sent then the following statement will be true
    elif(is_completed != None and is_confirmed == None):
        return order_restaurant_get_completed()


# ----------------------------------------------------------------------------------------------------------------------------
# the following will confirm the non confirmed order
def order_rest_patch_confirm():
    # will check for true value for is confirm to send the request to confirm the order
    if(request.json['is_confirmed'] in ['true','True']):
        data_one = 1
    elif(request.json['is_confirmed'] in ['false','False']):
        return make_response(json.dumps('false is not allowed for is_confirmed',default=str),400)
        # will senf the request on true data value
    results = conn_exe_close('call order_restaurant_patch_confirmed(?,?,?)',
    [request.json['order_id'],data_one,request.headers['token']])
    # if results is 1 then the it means the row was updated and order is confirmed
    # will show the following message 
    if(type(results) == list and results[0]['row_count'] == 1 ):
        return make_response(json.dumps('order confirmed',default=str),200)
    # if response row count is 0 then it is possible that order is already confirmed 
    elif(type(results) == list and results[0]['row_count'] == 0):
        return make_response(json.dumps('not confirmed or already confirmed',default=str),400)
    else:
        # if server error then error code 500 will show up
        return make_response(json.dumps(results,default=str),500)

# the following will complete and confirm the order on sending the is complete true
def order_rest_patch_complete():
    # will check if value is true and save 1 inside data_one to use that to send as a boolean for a request
    if(request.json['is_completed'] in ['true','True']):
        data_one = 1
        # if false is sent then simply error will be displayed
    elif(request.json['is_completed'] in ['false','False']):
        return make_response(json.dumps('false not allowed for is_completed',default=str),400)
    # send the request to update the is_complete which will automatically change the
    # is confirmed to true if not confirmed before
    results = conn_exe_close('call order_restaurant_patch_completed(?,?,?)',
    [request.json['order_id'],data_one,request.headers['token']])
    # if results have 1 then the row is changed
    if(type(results) == list and results[0]['row_count'] == 1 ):
        return make_response(json.dumps('order completed',default=str),200)
        # if the result is 0 then row is not changed or order might be completed already
    elif(type(results) == list and results[0]['row_count'] == 0):
        return make_response(json.dumps('complete request failed or already completed',default=str),400)
    else:
        # if error in server then code 500 will be shown
        return make_response(json.dumps(results,default=str),500)


def restaurant_patch():
    # will check for header token not sent or sent 
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        # if header is not sent then error will show up
        return make_response(json.dumps(invalid_header,default=str),400)
    invalid = verify_endpoints_info(request.json,['order_id'])
    if(invalid != None):
        # if order_id is not sent then error will show up
        return make_response(json.dumps(invalid,default=str),400)
    # saved the values just to make the checking easier for conditional
    is_confirmed = request.json.get('is_confirmed')
    is_completed = request.json.get('is_completed')
    # if only is confirmed is sent then this statement will be true
    if(is_confirmed != None):
        return order_rest_patch_confirm()
    # if only is completed is sent then this statement will be true
    elif(is_completed != None):
        return order_rest_patch_complete()
    # if both sent then this statement will be true
    elif(is_completed != None and is_confirmed != None):
        return order_rest_patch_complete()


    