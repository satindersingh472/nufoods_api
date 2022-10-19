import json
from webbrowser import get
from flask import request,make_response
from dbhelpers import conn_exe_close
from apihelpers import get_display_results,verify_endpoints_info

def all_clients():
    results = get_display_results('call all_clients()',[])
    results_json = make_response(json.dumps(results,default=str),200)
    return results_json