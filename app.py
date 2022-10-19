# import flask for api
from flask import Flask
# import dbcreds to check for production mode
import dbcreds
# import client.py for client endpoints
from clients import specific_client,add_client

app = Flask(__name__)

# get request for all clients
@app.get('/api/client')
def use_specific_client():
    return specific_client()

@app.post('/api/client')
def use_add_client():
    return add_client()


if(dbcreds.production_mode == True):
    print('Running in PRODUCTION MODE')
    import bjoern #type: ignore
    bjoern.run(app,'0.0.0.0',5001)
else:
    from flask_cors import CORS
    CORS(app)
    print('Running in TESTING MODE')
    app.run(debug=True)


