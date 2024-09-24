from flask import Flask, render_template, jsonify, request
import os
from openai import OpenAI
import random

app = Flask(__name__)

# Initialize the OpenAI client with the API key from the environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Define the standard 78-card tarot deck (Major and Minor Arcana)
tarot_deck = [
    # Major Arcana (22 cards)
    'The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor', 
    'The Hierophant', 'The Lovers', 'The Chariot', 'Strength', 'The Hermit', 
    'Wheel of Fortune', 'Justice', 'The Hanged Man', 'Death', 'Temperance', 
    'The Devil', 'The Tower', 'The Star', 'The Moon', 'The Sun', 
    'Judgement', 'The World',

    # Minor Arcana - Cups (14 cards)
    'Ace of Cups', 'Two of Cups', 'Three of Cups', 'Four of Cups', 'Five of Cups', 
    'Six of Cups', 'Seven of Cups', 'Eight of Cups', 'Nine of Cups', 'Ten of Cups', 
    'Page of Cups', 'Knight of Cups', 'Queen of Cups', 'King of Cups',

    # Minor Arcana - Pentacles (14 cards)
    'Ace of Pentacles', 'Two of Pentacles', 'Three of Pentacles', 'Four of Pentacles', 
    'Five of Pentacles', 'Six of Pentacles', 'Seven of Pentacles', 'Eight of Pentacles', 
    'Nine of Pentacles', 'Ten of Pentacles', 'Page of Pentacles', 'Knight of Pentacles', 
    'Queen of Pentacles', 'King of Pentacles',

    # Minor Arcana - Swords (14 cards)
    'Ace of Swords', 'Two of Swords', 'Three of Swords', 'Four of Swords', 
    'Five of Swords', 'Six of Swords', 'Seven of Swords', 'Eight of Swords', 
    'Nine of Swords', 'Ten of Swords', 'Page of Swords', 'Knight of Swords', 
    'Queen of Swords', 'King of Swords',

    # Minor Arcana - Wands (14 cards)
    'Ace of Wands', 'Two of Wands', 'Three of Wands', 'Four of Wands', 'Five of Wands', 
    'Six of Wands', 'Seven of Wands', 'Eight of Wands', 'Nine of Wands', 'Ten of Wands', 
    'Page of Wands', 'Knight of Wands', 'Queen of Wands', 'King of Wands'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shuffle', methods=['POST'])
def shuffle_deck():
    data = request.json
    spread = int(data.get('spread', 1))  # Number of cards to draw (default to 1)
    shuffled_deck = random.sample(tarot_deck, len(tarot_deck))  # Shuffle the deck
    drawn_cards = shuffled_deck[:spread]  # Draw the number of cards based on the spread

    return jsonify({'cards': drawn_cards})

@app.route('/tarot', methods=['POST'])
def tarot():
    data = request.json
    cards = data.get('cards', [])
    insight = data.get('insight', '')

    readings = []
    for card in cards:
        # Use OpenAI's Chat API to generate the tarot card reading, with the user's insight in mind
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a tarot reader."},
                {"role": "user", "content": f"Tell me about the tarot card {card} in relation to {insight}."}
            ]
        )
        response_message = response.choices[0].message.content
        readings.append({'card': card, 'reading': response_message})

    return jsonify({'readings': readings})

if __name__ == '__main__':
    app.run(debug=True)
