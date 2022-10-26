import json
from dbhelpers import conn_exe_close
from flask import request,make_response
from apihelpers import verify_endpoints_info

# will post the order for a client
def client_post():
    # will check if header is sent
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
    invalid = verify_endpoints_info(request.json,['menu_items','restaurant_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    order_post = conn_exe_close('call order_post(?,?)',[request.json.get('restaurant_id'),request.headers.get('token')])
    if(type(order_post) == list and len(order_post) == 1):
        menu_items = request.json.get('menu_items')
        for menu_item in menu_items:
            results = conn_exe_close('call orders_menus_post(?,?)',[order_post[0][0],menu_item])
        if(type(results) == list):
            return make_response(json.dumps(results,default=str),200)
        elif(type(results) == str):
            return make_response(json.dumps(results,default=str),400)
        else:
            return make_response(json.dumps(results,default=str),500)
    elif(type(order_post) == str):
        return make_response(json.dumps(order_post,default=str),400)
    else:
        return make_response(json.dumps(order_post,default=str),500)


def order_get():
    results = conn_exe_close('call order_get(?)',[request.headers.get('token')])
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)
    
def order_confirmed():
    if(request.args.get('is_confirmed') == True or 'true'):
        request.args.get('is_confirmed') == 1
    elif(request.args.get('is_confirmed') == False or 'false'):
        request.args.get('is_confirmed') == 0

    results = conn_exe_close('call order_confirmed(?,?)',request.headers.get('token'),request.args.get('is_confirmed'))
    if(type(results) == list):
        return make_response(json.dumps(results,default=str),200)
    elif(type(results) == str):
        return make_response(json.dumps(results,default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)
    


        