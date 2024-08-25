from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Dummy database
bus_location = {'latitude': 51.505, 'longitude': -0.09}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('startRide')
def handle_start_ride(data):
    emit('locationUpdate', bus_location, broadcast=True)

@socketio.on('updateLocation')
def handle_location_update(data):
    bus_location['latitude'] = data['latitude']
    bus_location['longitude'] = data['longitude']
    emit('locationUpdate', bus_location, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
