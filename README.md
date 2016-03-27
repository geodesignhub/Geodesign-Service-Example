## Geodesign-Service-Example
A example geodesign Impacts service that can be linked to Geodesign Hub. Once deployed on Heroku or similar services, it will seamlessly interoprate with Geodesign Hub. Geodesign Hub will send geometry information to the service and the service sends back impacts information to be displayed at the time of design. 

This is a Python [Flask](http://flask.pocoo.org/) service and also provides basic service authentication. It also has a Heroku geo enabled buildpack along with SciPy and Python stack. It may be used if you plan to use [Shapely](https://pypi.python.org/pypi/Shapely), [Rasterio](https://pypi.python.org/pypi/rasterio) or [Fiona](https://pypi.python.org/pypi/Fiona/) or other Python libraries.  

#### To create and deploy your own geodesign service
1. Fork this repository.
2. Modify config.py to have your own account credentials. You can get your Geodesign Hub API key [here](https://www.geodesignhub.com/api/token/) and you must be a participant to the project that this service submits data to.
3. Review the [post](https://github.com/geodesignhub/Geodesign-Service-Example/blob/master/app.py#L69) method in app.py, and modify accordingly with your code. 
4. Deploy to Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


In case you plan to use the buildpacks use the command below on Heroku to trigger multiple buildpacks
```
heroku buildpacks:set https://github.com/ddollar/heroku-buildpack-multi.git
```
