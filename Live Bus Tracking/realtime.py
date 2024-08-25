from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('student_transport.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/update_bus_location', methods=['POST'])
def update_bus_location():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bus_location (latitude, longitude)
        VALUES (?, ?)
    ''', (latitude, longitude))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'}), 200

@app.route('/update_student_location', methods=['POST'])
def update_student_location():
    data = request.json
    student_id = data['student_id']
    latitude = data['latitude']
    longitude = data['longitude']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO student_location (student_id, latitude, longitude)
        VALUES (?, ?, ?)
    ''', (student_id, latitude, longitude))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'}), 200

@app.route('/check_proximity', methods=['GET'])
def check_proximity():
    student_id = request.args.get('student_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get latest bus location
    cursor.execute('''
        SELECT latitude, longitude FROM bus_location
        ORDER BY timestamp DESC
        LIMIT 1
    ''')
    bus_location = cursor.fetchone()
    
    if not bus_location:
        return jsonify({'status': 'error', 'message': 'No bus location found'}), 404
    
    bus_lat, bus_lon = bus_location['latitude'], bus_location['longitude']
    
    # Get latest student location
    cursor.execute('''
        SELECT latitude, longitude FROM student_location
        WHERE student_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    ''', (student_id,))
    student_location = cursor.fetchone()
    
    if not student_location:
        return jsonify({'status': 'error', 'message': 'No student location found'}), 404
    
    student_lat, student_lon = student_location['latitude'], student_location['longitude']
    
    # Calculate distance
    distance = calculate_distance(bus_lat, bus_lon, student_lat, student_lon)
    
    return jsonify({'distance': distance}), 200

def calculate_distance(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2
    R = 6371  # Radius of Earth in km
    
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c

if __name__ == '__main__':
    app.run(debug=True)
