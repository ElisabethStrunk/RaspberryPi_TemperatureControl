import os
from multiprocessing import Process
from flask import Flask, render_template, make_response
from flask_restful import Api, Resource, reqparse
from flask_socketio import SocketIO

from temperature_sensor import get_temperature

# Initialise app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)


# Define restful resources
class TemperatureResource(Resource):
    parser = reqparse.RequestParser()
    #parser.add_argument('temperature', type=str)
    parser.add_argument('html', type=str, location='args')

    def get(self):
        try:
            temperature = get_temperature()
            if TemperatureResource.parser.parse_args()['html']:
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template('temperature.html', temperature=temperature), 200, headers)
            else:
                return {'status': temperature}, 200
        except Exception:
            return {'message': 'An error occurred fetching the temperature. {}'.format(e)}, 500

    #def put(self):
    #    try:
    #        try:
    #            data = TemperatureResource.parser.parse_args()['temperature']
    #        except Exception:
    #            return {'message': 'No temperature data received.'}, 400
    #        if set_temperature(data):
    #            return {'message': '{} is not a valid temperature'.format(data)}, 400
    #        return {'message': 'Target temperature changed to {}'.format(data)}, 200
    #    except Exception as e:
    #        return {'message': 'An error occurred during changing the target temperature. {}'.format(e)}, 500

# Initialise restful api
api = Api()
api.add_resource(TemperatureResource, '/temperature')
api.init_app(app)

# Initialise flask-socketio
socketio = SocketIO()
socketio.init_app(app)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
