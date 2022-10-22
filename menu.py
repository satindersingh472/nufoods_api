import json
from flask import request,make_response
import json
from apihelpers import verify_endpoints_info
from dbhelpers import conn_exe_close

# all menu will return the menu items associated with a particular restaurant
def all_menu():
    invalid = verify_endpoints_info(request.args,['restaurant_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = conn_exe_close('call all_menu(?)',[request.args.get('restaurant_id')])
    results_json = make_response(json.dumps(results,default=str),200)
    return results_json