from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

USERNAME = 'crazyrider'
PASSWORD = 'AirbusA320!'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(f"API Response Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data and 'states' in data:
            flights = []
            for state in data['states']:
                flight = {
                    'icao24': state[0],
                    'callsign': state[1].strip() if state[1] else "N/A",
                    'country': state[2],
                    'longitude': state[5],
                    'latitude': state[6],
                    'altitude': state[7],
                    'velocity': state[9],
                    'true_track': state[10] if state[10] is not None else 0  # Include true_track as heading
                }
                flights.append(flight)
            return jsonify(flights)
        else:
            return jsonify([])  # Return an empty list if no data
    else:
        return jsonify([])  # Return an empty list if the API call fails

@socketio.on('connect')
def handle_connect():
    print("Client connected")

if __name__ == '__main__':
    socketio.run(app, debug=True)
