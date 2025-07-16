import os
from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
from flask_cors import CORS # Import CORS for cross-origin requests

app = Flask(__name__)
CORS(app)

# Get API key from environment variable or use placeholder
API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')

if not API_KEY or API_KEY == 'YOUR_GEMINI_API_KEY_HERE':
    print("Error: GEMINI_API_KEY is not set or is still the placeholder.") 
    print("Please set your GEMINI_API_KEY environment variable or replace 'YOUR_GEMINI_API_KEY_HERE' with your actual API key.")
    exit()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    
    try:
        data = request.get_json()
        user_message = data.get('message')
        # The history from the frontend will be in the format expected by Gemini API
        # e.g., [{"role": "user", "parts": [{"text": "..."}]}, {"role": "model", "parts": [{"text": "..."}]}]
        chat_history = data.get('history', [])

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Start a chat session with the provided history
        # The Gemini model will use this history to maintain context
        chat_session = model.start_chat(history=chat_history)

        # Send the user's message to the Gemini model
        response = chat_session.send_message(user_message)

        # Extract the bot's response text
        bot_response_text = response.text

        # The chat_session.history now contains the updated conversation,
        # including the latest user and model messages.
        # Convert the history to JSON-serializable format
        updated_chat_history = []
        for message in chat_session.history:
            updated_chat_history.append({
                "role": message.role,
                "parts": [{"text": part.text} for part in message.parts]
            })

        return jsonify({
            "response": bot_response_text,
            "history": updated_chat_history
        })

    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred in /chat: {e}")
        # Return a generic error message to the frontend
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the Flask app
    # debug=True allows for automatic reloading on code changes
    # host='0.0.0.0' makes the server accessible from other devices on the network
    # port=5000 is the default Flask port
    app.run(debug=True, host='127.0.0.1', port=5000)

