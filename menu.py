import json
from flask import request,make_response
import json
from apihelpers import verify_endpoints_info
from dbhelpers import conn_exe_close

# all menu will return the menu items associated with a particular restaurant
def all_menu():
    # will check for restaurant id if it is sent
    invalid = verify_endpoints_info(request.args,['restaurant_id'])
    # if restaurant id not sent then error will show up
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = conn_exe_close('call all_menu(?)',[request.args.get('restaurant_id')])
    # if menu exists then it return a list of one or more menu items
    if(type(results) == list and len(results) >= 1):
        return make_response(json.dumps(results,default=str),200)
        # if no menu exists then list will be empty
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps('sorry no menu available',default=str),200)
    elif(type(results) == str):
        # if something goes wrong an error will display
        return make_response(json.dumps(results,default=str),400)
    else:
        # if something is wrong with server then 500 code will show
        return make_response(json.dumps(results,default=str),500)


def menu_post():
    # will check if token is sent as headers
    invalid_header = verify_endpoints_info(request.headers,['token'])
    # if not then the following statement will become true
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
        # will check if other data is sent or no
        # if not then error will show up
    invalid = verify_endpoints_info(request.json,['name','price','description','image_url'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = conn_exe_close('call menu_post(?,?,?,?,?)',
    [request.json.get('name'),request.json.get('price'),request.json.get('description'),
    request.json.get('image_url'),request.headers.get('token')])
    # if item added it will return the menu item id
    if(type(results)==list and len(results) == 1):
        return make_response(json.dumps(results[0][0],default=str),200)
    elif(type(results) == list and len(results) == 0):
        # if not then error message will appear
        return make_response(json.dumps('no item added',default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)
    