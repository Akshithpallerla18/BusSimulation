// WebSocket setup
const socket = io.connect('http://localhost:5000');

// Listen for location updates
socket.on('location_update', function(data) {
    const { latitude, longitude, type } = data;
    if (type === 'bus') {
        // Update bus location on the map
    } else if (type === 'student') {
        // Update student location on the map
    }
});
