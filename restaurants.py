import json
from flask import request,make_response
import json
from dbhelpers import conn_exe_close
from apihelpers import verify_endpoints_info

# all restaurants will fulfill the get request and will get all the restaurants without any id given
def all_restaurants():
    results = conn_exe_close('call all_restaurants()',[])
    results_json = make_response(json.dumps(results,default=str),200)
    return results_json

# specific restaurant will return the restaurant with specific id given as a param
# this function will fulfill the get request
def specific_restaurant():
    invalid = verify_endpoints_info(request.args,['restaurant_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    results = conn_exe_close('call specific_restaurant(?)',[request.args.get('restaurant_id')])
    results_json = make_response(json.dumps(results,default=str),200)
    return results_json

