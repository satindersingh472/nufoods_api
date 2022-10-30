import json
from dbhelpers import conn_exe_close
from flask import request,make_response
from apihelpers import verify_endpoints_info

# will post the order for a client
def client_post():
    # will check if header is sent
    invalid_header = verify_endpoints_info(request.headers,['token'])
    # if not sent then the error will show up
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
        # check for various data arguments if not sent then an error will show up
    invalid = verify_endpoints_info(request.json,['menu_items','restaurant_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
        # will make a request to get back the order id
    order_post = conn_exe_close('call order_post(?,?)',[request.json['restaurant_id'],request.headers['token']])
    # use the order to post a menu
    if(type(order_post) == list and len(order_post) == 1):
        # menu items will be array that is sent with menu item ids
        menu_items = request.json.get('menu_items')
        # will loop through menu items and send a request for each menu item with id
        # by using order id and menu item id
        for menu_item in menu_items:
            results = conn_exe_close('call orders_menus_post(?,?)',[order_post[0]['order_id'],menu_item])
            # after the loop finishes it will show the results as id of the order posted
        if(type(results) == list):
            return make_response(json.dumps(results[0],default=str),200)
        elif(type(results) == str):
            # if error it will show the error with a code 400
            return make_response(json.dumps(results,default=str),400)
        else:
            # if there is any other error besides user input or database the server error will show up
            return make_response(json.dumps(results,default=str),500)
    elif(type(order_post) == str or len(order_post) != 1):
        # if order post not able to bring back the if of an order
        # then this result will be shown
        return make_response(json.dumps(order_post,default=str),400)
    else:
        # or if there is any other error wit server regarding order post call it will show this error 
        return make_response(json.dumps(order_post,default=str),500)



# order_get will get all the orders associated with a client
# either confirmed,not confirmed, completed and not completed
def order_get():
    # will send the request to grab the orders related to the specific token
    results = conn_exe_close('call order_get(?)',[request.headers.get('token')])
    if(type(results) == list):
        # if result is list then this response is shown
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        # if error then this response is shown
        return make_response(json.dumps(results,default=str),400)
    else:
        # or else for server error the following response is shown
        return make_response(json.dumps(results,default=str),500)


# order_confirmed is used for sending request to get the confirmed order either not confirmed or confirmed
def order_confirmed():
    # will expect argument is_confirmed and check for value
    # if value is true then 1 is sent to the database
    # if value is false then 0 is sent to the database
    if(request.args['is_confirmed'] in ['true','True']):
        data = 1
    elif(request.args['is_confirmed'] in ['False','false']):
        data = 0
        # will send the request with valid header and is_confirmed value
    results = conn_exe_close('call order_confirmed(?,?)',[request.headers['token'],data])
    if(type(results) == list):
        # if results is a list then following response will be shown
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        # if error in results then this response will be shown
        return make_response(json.dumps(results,default=str),400)
    else:
        # if server error then this reponse will be shown
        return make_response(json.dumps(results,default=str),500)

def order_completed():
    if(request.args['is_completed'] in ['true','True']):
        data = 1
    elif(request.args['is_completed'] in ['false','False']):
        data = 0
    results = conn_exe_close('call order_completed(?,?)',[request.headers['token'],data])
    if(type(results) == list):
        # if results is a list then following response will be shown
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        # if error in results then this response will be shown
        return make_response(json.dumps(results,default=str),400)
    else:
        # if server error then this reponse will be shown
        return make_response(json.dumps(results,default=str),500)

    
def order_complete_confirmed():
    # check if is complete is true and then if true data sent will be 1
    if(request.args['is_completed'] in ['true','True']):
        data_one = 1
        # if false then data sent will be 0
    elif(request.args['is_completed'] in ['false','False']):
        data_one = 0
        # check if is confirmed is true and then data sent will be 1
    if(request.args['is_confirmed'] in ['true','True']):
        data_two = 1
        # if false then data sent is 0
    elif(request.args['is_confirmed'] in ['false','False']):
        data_two = 0
        # send the request to the database
    results = conn_exe_close('call order_complete_confirmed(?,?,?)',[request.headers['token'],data_one,data_two])
    if(type(results) == list):
        # if results is a list then following response will be shown
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        # if error in results then this response will be shown
        return make_response(json.dumps(results,default=str),400)
    else:
        # if server error then this reponse will be shown
        return make_response(json.dumps(results,default=str),500)    

    
def client_get():
    # check if valid header is sent with token
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        # if token not sent as a header then error will show up
        return make_response(json.dumps(invalid_header,default=str),400)
    # store the value of arguments to make the process of checking easier
    is_confirmed = request.args.get('is_confirmed')
    is_completed = request.args.get('is_completed')
    # if no data is sent regarding confirm or complete then all orders will be displayed
    if(is_completed == None and is_confirmed == None):
        return order_get()
        # if both arguments sent will check for conditions and send the appropridate data
    elif(is_completed != None and is_confirmed != None):
        return order_complete_confirmed()
        # if only confirmed is asked this condition will become true
    elif(is_confirmed != None and is_completed == None):
        return order_confirmed()
        # if only completed is asked this will be true
    elif(is_completed != None and is_confirmed == None):
        return order_completed()
    

        