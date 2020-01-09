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


class TemperatureDatabase:
    @classmethod
    def create_temperature_tables(cls):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        create_table = "CREATE TABLE IF NOT EXISTS temperature (target REAL, tolerance REAL)"
        cursor.execute(create_table)
        cursor.execute("INSERT INTO temperature VALUES (23.0, 3.0)")
        connection.commit()
        connection.close()

    @classmethod
    def read_target_temperature(cls):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        query = "SELECT target from temperature"
        result = cursor.execute(query)
        target = result.fetchone()
        connection.close()
        return target[0]

    @classmethod
    def write_target_temperature(cls, new_target_temperature):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        query = "UPDATE temperature SET target=?"
        cursor.execute(query, (new_target_temperature,))
        connection.commit()
        connection.close()

    @classmethod
    def read_temperature_tolerance(cls):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        query = "SELECT tolerance from temperature"
        result = cursor.execute(query)
        tolerance = result.fetchone()
        connection.close()
        return tolerance[0]

    @classmethod
    def write_temperature_tolerance(cls, new_temperature_tolerance):
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        query = "UPDATE temperature SET tolerance=?"
        cursor.execute(query, (new_temperature_tolerance,))
        connection.commit()
        connection.close()

# Create data base if it does not already exist
if not os.path.exists(db_file):
    print('Could not find {}, creating new file'.format(db_file))
    TemperatureDatabase.create_temperature_tables()


# Define restful resources
class TemperatureResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('target', type=str)
    parser.add_argument('tolerance', type=str)
    parser.add_argument('html', type=str, location='args')

    def get(self):
        try:
            temperature = get_temperature()
            if TemperatureResource.parser.parse_args()['html']:
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template('temperature.html',
                                                     temperature=temperature,
                                                     target=TemperatureDatabase.read_target_temperature(),
                                                     tolerance=TemperatureDatabase.read_temperature_tolerance()
                                                     ), 200, headers)
            else:
                return {'temperature': temperature,
                        'target': TemperatureDatabase.read_target_temperature(),
                        'tolerance': TemperatureDatabase.read_temperature_tolerance()}, 200
        except Exception as e:
            return {'message': 'An error occurred fetching temperature information. {}'.format(e)}, 500

    def post(self):
        try:
            arguments = TemperatureResource.parser.parse_args()
            if arguments['target']:
                target = arguments['target']
                TemperatureDatabase.write_target_temperature(float(target))
            if arguments['tolerance']:
                tolerance = arguments['tolerance']
                TemperatureDatabase.write_target_temperature(float(tolerance))

            if arguments['html']:
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template('temperature.html',
                                                     target=TargetTemperatureDatabase.read_target_temperature()
                                                     target=TemperatureDatabase.read_target_temperature(),
                                                     tolerance=TemperatureDatabase.read_temperature_tolerance()
                                                     ), 200, headers)
            else:
                message = ''
                if arguments['target']:
                    message = message + 'Target temperature changed to {}'.format(target)
                if arguments['tolerance']:
                    message = message + 'Temperature tolerance changed to {}'.format(tolerance)
                return {'message': message}, 200
        except Exception as e:
            return {'message': 'An error occurred during changes in the temperature configurations. '
                               '{}'.format(e)}, 500

# Initialise restful api
api = Api()
api.add_resource(TemperatureResource, '/temperature')
api.init_app(app)

# Initialise flask-socketio
socketio = SocketIO()
socketio.init_app(app)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
