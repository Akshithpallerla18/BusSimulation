from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@app.route('/start_tracking')
def start_tracking():
    emit('start_tracking', broadcast=True)
    return jsonify({'status': 'tracking started'}), 200

@socketio.on('update_location')
def handle_location_update(data):
    emit('location_update', data, broadcast=True)
