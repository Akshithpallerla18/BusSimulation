// Initialize the map
var map = L.map('map').setView([51.505, -0.09], 13);  // Default coordinates

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

var marker;

// WebSocket or AJAX connection for real-time updates
var socket = new WebSocket('ws://your-server-url');  // Replace with your WebSocket server URL

socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var lat = data.latitude;
    var lon = data.longitude;
    
    // Update the map with the new location
    if (marker) {
        marker.setLatLng([lat, lon]);
    } else {
        marker = L.marker([lat, lon]).addTo(map);
    }
    map.setView([lat, lon], 13);

    // Check distance and send notification
    var distance = calculateDistance(lat, lon, studentLat, studentLon);  // Replace with student's coordinates
    if (distance <= 3) {
        document.getElementById('notification').textContent = 'Bus is 3 km away!';
    }
};

// Start ride button event
document.getElementById('start-ride').addEventListener('click', function() {
    socket.send(JSON.stringify({action: 'startRide'}));
});

// Function to calculate distance (Haversine formula)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the Earth in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;  // Distance in km
}
