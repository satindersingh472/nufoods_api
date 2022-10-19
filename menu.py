import json
from flask import request,make_response
import json
from apihelpers import get_display_results,verify_endpoints_info

# all menu will return the menu items associated with a particular restaurant
def all_menu():
    invalid = verify_endpoints_info(request.args,['restaurant_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = get_display_results('call all_menu(?)',[request.args.get('restaurant_id')])
    results_json = make_response(json.dumps(results,default=str),200)
    return results_json