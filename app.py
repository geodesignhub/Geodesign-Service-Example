from flask import Flask, url_for
from functools import wraps
from flask import request, Response
import json, geojson, requests
import random,os
import GeodesignHub

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
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
    return 'Welcome to Geodesign Impacts Service'

@app.route('/post', methods = ['POST'])
@requires_auth
def post():
    if request.headers['Content-Type'] == 'application/json':
        pass
    else:
        msg = {"message":"Unsupported Media Type"}
        return Response(json.dumps(msg), status=415, mimetype='application/json')

    req = json.loads(request.data)
    try:
        jobid = req['jobid']
        callback = req['callback']
        geometries = req['geometry']
    except KeyError as e:
        msg = json.dumps({"message":"Jobid, callback or geometries data not found. These are required fields in your JSON."})
        return Response(msg, status=400, mimetype='application/json')

    gjData = geojson.loads(json.dumps(geometries))
	# validate geojson
    validation = geojson.is_valid(gjData)
	# if gj is valid

    if validation['valid'] == 'yes':

        # Assuming that it is a feature collection
        impactsAssignmentList = ['orange', 'orange2', 'yellow','purple', 'purple2']
        allFeats = []
        for feature in gjData['features']:
            feature['properties']['areatype'] = random.choice(impactsAssignmentList)
            allFeats.append(feature)

        fc = {"type":"FeatureCollection", "features":allFeats}
    	myAPIHelper = GeodesignHub.GeodesignHubClient(url = 'https://www.geodesignhub.com/api/v1/', project_id='91cb24d7cd1feb2b', token='6858b59a256e5dc0028dd3261dafb2e1c1ead912')
    	upload = myAPIHelper.post_gdservice_JSON(geometry=fc, jobid=jobid)
        print upload.status_code

    else:
        msg = json.dumps({"message":"Invalid GeoJSON submitted."})
        return Response(msg, status=400, mimetype='application/json')


    op = json.dumps ({"message":"OK"})
    return Response(op, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5001))
    app.run(port =port)

