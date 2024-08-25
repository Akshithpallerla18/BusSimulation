// Update bus location
function updateBusLocation(lat, lon) {
    fetch('/update_bus_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            latitude: lat,
            longitude: lon
        })
    });
}

// Update student location
function updateStudentLocation(studentId, lat, lon) {
    fetch('/update_student_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            student_id: studentId,
            latitude: lat,
            longitude: lon
        })
    });
}

// Check proximity
function checkProximity(studentId) {
    fetch(`/check_proximity?student_id=${studentId}`)
        .then(response => response.json())
        .then(data => {
            if (data.distance <= 3) {
                alert('The bus is within 3 km of your location!');
            }
        });
}
