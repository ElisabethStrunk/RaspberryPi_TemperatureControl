import os
import sqlite3
from multiprocessing import Process
from flask import Flask, render_template, make_response
from flask_restful import Api, Resource, reqparse
from flask_socketio import SocketIO

from temperature_sensor import get_temperature

# Initialise app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)


# Data base
db_file = 'data.db' #'/home/pi/temp_ctrl/data.db'


class TargetTemperatureDatabase:
    @classmethod
    def create_target_temperature_table(cls):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        create_table = "CREATE TABLE IF NOT EXISTS temperature (target REAL)"
        cursor.execute(create_table)
        cursor.execute("INSERT INTO temperature VALUES (23.0)")
        connection.commit()
        connection.close()

    @classmethod
    def read_target_temperature(cls):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        query = "SELECT target from temperature"
        result = cursor.execute(query)
        status = result.fetchone()
        connection.close()
        return status[0]

    @classmethod
    def write_target_temperature(cls, new_target_temperature):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        query = "UPDATE temperature SET target=?"
        cursor.execute(query, (new_target_temperature,))
        connection.commit()
        connection.close()


# Create data base if it does not already exist
if not os.path.exists(db_file):
    print('Could not find {}, creating new file'.format(db_file))
    TargetTemperatureDatabase.create_target_temperature_table()


# Define restful resources
class TemperatureResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('target', type=str)
    parser.add_argument('html', type=str, location='args')

    def get(self):
        try:
            temperature = get_temperature()
            if TemperatureResource.parser.parse_args()['html']:
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template('temperature.html',
                                                     temperature=temperature,
                                                     target=TargetTemperatureDatabase.read_target_temperature()
                                                     ), 200, headers)
            else:
                return {'status': temperature}, 200
        except Exception:
            return {'message': 'An error occurred fetching the temperature. {}'.format(e)}, 500

    def post(self):
        try:
            try:
                data = TemperatureResource.parser.parse_args()['target']
            except Exception:
                return {'message': 'No temperature data received.'}, 400
            TargetTemperatureDatabase.write_target_temperature(float(data))

            if TemperatureResource.parser.parse_args()['html']:
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template('temperature.html',
                                                     temperature=get_temperature(),
                                                     target=TargetTemperatureDatabase.read_target_temperature()
                                                     ), 200, headers)
            else:
                return {'message': 'Target temperature changed to {}'.format(data)}, 200
        except Exception as e:
            return {'message': 'An error occurred during changing the target temperature. {}'.format(e)}, 500

# Initialise restful api
api = Api()
api.add_resource(TemperatureResource, '/temperature')
api.init_app(app)

# Initialise flask-socketio
socketio = SocketIO()
socketio.init_app(app)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
