import json
from dbhelpers import conn_exe_close
from flask import request,make_response
from apihelpers import verify_endpoints_info

# 
def client_post():
    invalid_header = verify_endpoints_info(request.headers,['token'])
    if(invalid_header != None):
        return make_response(json.dumps(invalid_header,default=str),400)
    invalid = verify_endpoints_info(request.json,['menu_items','restaurant_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid,default=str),400)
    