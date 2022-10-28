import json
from flask import request,make_response
from apihelpers import verify_endpoints_info,add_for_patch
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
        # if item not added then the list will be returned with lenght 0
    elif(type(results) == list and len(results) == 0):
        # if not then error message will appear
        return make_response(json.dumps('no item added',default=str),400)
    else:
        # if there is a server error then it will be shown as a error with 500 code
        return make_response(json.dumps(results,default=str),500)
    

# will delete an item from the restaurant side
# a restaurant will valid token and menu id is needed
def menu_delete():
    # token will be sent as a header and this will check if it is sent or not
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        # if not then error is sent back
        return make_response(json.dumps(invalid_header,default=str),400)
        # check if menu id is sent
    invalid = verify_endpoints_info(request.json,['menu_id'])
    if(invalid != None):
        # if not then error is sent
        return make_response(json.dumps(invalid,default=str),400)
        # if menu id is sent as a data then request is performed
    results = conn_exe_close('call menu_delete(?,?)',
    [request.json.get('menu_id'),request.headers.get('token')])
    # the procedure sends back the row count and if it is 1 then something is deleted
    if(type(results) == list and results[0][0] == 1):
        return make_response(json.dumps('menu item deleted',default=str),200)
        # if not one or 0 then menu item is not deleted
    elif(type(results) == list and results[0][0] == 0):
        return make_response(json.dumps('menu item not exists or user is not authorized',default=str),400)
    else:
        # if server error then it will show the following message
        return make_response(json.dumps(results,default=str),500)

def menu_patch():
    # will check for the token sent as header if not then error but no errror on wrong token
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
    # menu_id is required so will check if it sent or not
    invalid = verify_endpoints_info(request.json,['menu_id'])
    # if menu id is not sent then we will return the function with error because menu_id is required
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    # need to grab the details about the menu item before any update
    menu_item_details = conn_exe_close('call menu_specific_id(?,?)',[request.json.get('menu_id'),request.headers.get('token')])
    # if menu_item_details gives back list and len is zero then function will return an error and dont proceed
    if(type(menu_item_details) != list or len(menu_item_details) == 0):
        return make_response(json.dumps(menu_item_details,default=str),400)
    # after getting details will call add for patch function to add original data to the request if everything is not sent
    menu_item = add_for_patch(request.json,['menu_id','name','price','description','image_url'],menu_item_details[0])
    # after editing the original data we will send the arguments the user wants to change and some original one as well
    # if not sent by the user just so that our stored procedure works fine with inputs
    results = conn_exe_close('call menu_patch(?,?,?,?,?,?)',
    [menu_item['menu_id'],menu_item['name'],menu_item['price'],menu_item['description'],menu_item['image_url'],request.headers.get('token')])
    if(type(results) == list):
        return make_response(json.dumps('menu is successfully updated',default=str),200)
    elif(type(results) != list):
        return make_response(json.dumps(f'menu not updated',default=str),400)
    else:
        return make_response(json.dumps(results,default=str),500)

    