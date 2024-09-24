from flask import Flask, render_template, jsonify, request
import os
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI client with the API key from the environment variable
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tarot', methods=['POST'])
def tarot():
    data = request.json
    card = data.get('card', 'Unknown')

    # Prepare the model and messages for OpenAI completion
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are a tarot reader."},
        {"role": "user", "content": f"Tell me about the tarot card {card}."}
    ]

    try:
        # Use the new API method for ChatCompletion
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0  # Ensure the response is deterministic
        )

        # Extract the response message
        response_message = response.choices[0].message.content
        print(response_message)  # Print the response for debugging

        # Return the response to the frontend
        return jsonify({'card': card, 'reading': response_message})

    except Exception as e:
        # Handle potential errors and return them
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
