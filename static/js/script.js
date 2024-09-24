function shuffleAndDraw() {
    // Get the user input and spread type
    var insight = document.getElementById('insight').value;
    var spread = document.getElementById('spread').value;

    // Prepare the POST request to shuffle the deck and draw the number of cards
    fetch('/shuffle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ insight: insight, spread: spread })  // Send user's input and spread choice
    })
    .then(response => response.json())
    .then(data => {
        const drawnCards = data.cards;
        document.getElementById('cards').innerHTML = `You drew: ${drawnCards.join(', ')}`;

        // Now that we have the drawn cards, request their readings
        getReadings(drawnCards, insight);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('cards').innerHTML = 'An error occurred while shuffling the deck.';
    });
}

function getReadings(cards, insight) {
    fetch('/tarot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cards: cards, insight: insight })  // Send the drawn cards and the insight question
    })
    .then(response => response.json())
    .then(data => {
        // Display the readings for the cards
        let readingsHtml = '';
        data.readings.forEach(reading => {
            readingsHtml += `<strong>${reading.card}:</strong> ${reading.reading}<br>`;
        });
        document.getElementById('result').innerHTML = readingsHtml;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = 'An error occurred while fetching the tarot reading.';
    });
}
