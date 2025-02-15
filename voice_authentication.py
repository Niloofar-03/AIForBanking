from flask import Flask, jsonify, session, request
import speech_recognition as sr
from app import compare_voices

app = Flask(__name__)

# Define the authorized phrase
AUTHORIZED_PHRASE = "my word is my password"

@app.route('/authenticate-voice')
def authenticate_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for authentication...")
        audio = recognizer.listen(source)

    # Save the recorded audio sample
    with open("user_sample.wav", "wb") as f:
        f.write(audio.get_wav_data())

    print("Voice sample saved.")

    # Now let's check the comparison
    result = compare_voices("user_sample.wav", "reference.wav")
    print(f"Voice comparison result: {result}")
    
    if result:
        session["authenticated"] = True
        return jsonify({"status": "success", "message": "Voice recognized!"})
    else:
        session["authenticated"] = False
        return jsonify({"status": "failure", "message": "Voice authentication failed."})

@app.route('/transfer', methods=["POST"])
def transfer_funds():
    # Check if the user is authenticated before proceeding
    if not session.get("authenticated"):
        return jsonify({"status": "failure", "message": "Authentication required to perform transaction."})

    recipient = request.json.get("recipient")
    amount = request.json.get("amount")
    
    if not recipient or not amount:
        return jsonify({"status": "failure", "message": "Please provide both recipient and amount."})
    
    # Process the transaction logic here (you can simulate it for now)
    print(f"Processing transaction: Sending {amount} to {recipient}")
    
    # Simulate successful transaction
    return jsonify({"status": "success", "message": f"Transaction successful. {amount} sent to {recipient}."})

if __name__ == '__main__':
    app.secret_key = 'your_secret_key_here'  # Ensure you have a secret key for session management
    app.run(debug=True)
