import json
from dbhelpers import conn_exe_close
from flask import request,make_response
from apihelpers import verify_endpoints_info

def order_restaurant_get():
    # will request the data only with token and bring back all the orders regardless 
    # of confirm or complete
    results = conn_exe_close('call order_restaurant_get(?)',[request.headers.get('token')])
    # list of results means a response is okay
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
