function getReading() {
    var cardName = document.getElementById('card').value;

    // Fetch request to the Flask backend
    fetch('/tarot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ card: cardName })
    })
    .then(response => response.json())
    .then(data => {
        // Display the result in the div
        document.getElementById('result').innerHTML = `<strong>Reading for ${data.card}:</strong> ${data.reading}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = 'An error occurred while fetching the tarot reading.';
    });
}
