## Geodesign-Service-Example
A example geodesign Impacts service that can be linked to Geodesign Hub. Once deployed on Heroku or similar services, it will seamlessly interoprate with Geodesign Hub. Geodesign Hub will send geometry information to the service and the service sends back impacts information to be displayed at the time of design. 

This uses Python [Flask](http://flask.pocoo.org/) and also provides basic service authentication. 

#### To create and deploy your own geodesign service
1. Fork this repository.
2. Modify config.py to have your own account credentials. You can get you Geodesign Hub API key [here](https://www.geodesignhub.com/api/token/)
3. Look at post method in app.py, and modify accordingly with your code. 
4. Deploy to Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
