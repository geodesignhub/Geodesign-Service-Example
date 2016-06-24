from flask import Flask, url_for
from functools import wraps
from flask import request, Response
import json, geojson, requests
import random,os
import GeodesignHub, config

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid. Please change it to one
    suitable for your service.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)

@app.route('/', methods = ['GET'])
@requires_auth
def api_root():
    ''' This is the root of the webservice, upon successful authentication a text will be displayed in the browser '''
    return 'Welcome to Geodesign Impacts Service'

@app.route('/post', methods = ['POST'])
@requires_auth
def post():
    ''' This is the main POST method that takes in a request from Geodesign Hub and processes the input data '''
    # check if the request headers are specified and the data sent are JSON
    if request.headers['Content-Type'] == 'application/json':
        pass
    else:
        # If the media type is not JSON, return a HTTP 415 message
        msg = {"message":"Unsupported Media Type"}
        return Response(json.dumps(msg), status=415, mimetype='application/json')
    # Load the JSON data from Geodesign Hub
    req = json.loads(request.data)
    # check that
    try:
        # check that the data coming in from Geodesign Hub has all the keys
        jobid = req['jobid']
        callback = req['callback']
        geometries = req['geometry']
        jobtype = req['type']
        projectname = req['projectname']
    except KeyError as e:
        msg = json.dumps({"message":"Four parameters are required: jobid, jobtype, callback, geometry and Geodesign Hub projectname. One or more of these were not found in your JSON request."})
        return Response(msg, status=400, mimetype='application/json')
    # Once the data has been verified, parse it.
    gjData = geojson.loads(json.dumps(geometries))
	# validate geojson
    validation = geojson.is_valid(gjData)
	# if geojson is  is valid

    if validation['valid'] == 'yes':
        # Implement your impacts code here. The code below takes all the features and assigns a random impacts to them.
        impactsAssignmentList = ['orange', 'orange2', 'yellow','purple', 'purple2']
        allFeats = []
        for feature in gjData['features']:
            feature['properties']['areatype'] = random.choice(impactsAssignmentList)
            allFeats.append(feature)
        # Once all features have been parsed, build a feature collection
        fc = {"type":"FeatureCollection", "features":allFeats}
        # Setup the API.
    	myAPIHelper = GeodesignHub.GeodesignHubClient(url = config.apisettings['serviceurl'], token=config.apisettings['apitoken'])
        # Send the impact geometries back to the project
    	upload = myAPIHelper.post_gdservice_JSON(geometry=fc, jobid=jobid)
        # if status code is 202 / Accepted then all Ok
        if upload.status_code == 202:
            pass

    else:
        # If invalid geoJSON is submitted, return a 400 message.
        msg = json.dumps({"message":"Invalid GeoJSON submitted."})
        return Response(msg, status=400, mimetype='application/json')

    op = json.dumps ({"message":"OK"})
    return Response(op, status=200, mimetype='application/json')
if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5001))
    app.run(port =port)
