from flask import Flask, render_template, jsonify, request, session
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import numpy as np

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key for session management
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Predefined secret phrase for authentication (never shown to the user)
AUTHORIZED_PHRASE = "My word is my password"
REFERENCE_VOICE_FILE = "reference.wav"  # Path to the reference voice file

def compare_voices(sample_file, reference_file):
    """Compare user voice sample with the reference voice."""
    sample_audio = AudioSegment.from_wav(sample_file)
    reference_audio = AudioSegment.from_wav(reference_file)

    # Extract loud sections
    sample_chunks = detect_nonsilent(sample_audio, min_silence_len=100, silence_thresh=-40)
    reference_chunks = detect_nonsilent(reference_audio, min_silence_len=100, silence_thresh=-40)

    if len(sample_chunks) == 0 or len(reference_chunks) == 0:
        return False  # No valid voice detected

    # Compare durations
    sample_length = np.mean([chunk[1] - chunk[0] for chunk in sample_chunks])
    reference_length = np.mean([chunk[1] - chunk[0] for chunk in reference_chunks])

    return abs(sample_length - reference_length) < 500  # Allow small variations

def record_voice_sample(filename="user_voice.wav"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say the Secret Key for authentication...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for the user's voice

        # Save the recorded audio to a WAV file
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

    print(f"User voice sample saved as {filename}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/authenticate-voice', methods=['POST'])
def authenticate_voice():
    # Record user's voice sample
    user_voice_file = "user_voice.wav"
    record_voice_sample(user_voice_file)

    # Compare with reference voice
    reference_file = "reference.wav"  # Path to the reference voice
    is_authenticated = compare_voices(user_voice_file, reference_file)

    if is_authenticated:
        session["authenticated"] = True  # Store in session
        return jsonify({"status": "success", "message": "Authentication successful!"})
    else:
        session["authenticated"] = False
        return jsonify({"status": "failure", "message": "Authentication failed! Please try again."})

@app.route('/transfer', methods=['POST'])
def transfer_funds():
    if not session.get("authenticated"):
        return jsonify({"status": "failure", "message": "You cannot perform a transaction because authentication failed."})

    # Retrieve transaction details from the request
    data = request.json
    amount = data.get("amount")
    recipient = data.get("recipient")

    if not amount or not recipient:
        return jsonify({"status": "failure", "message": "Invalid transaction details"})

    # Process the transaction (this is just a mock for now)
    session["authenticated"] = False  # Reset authentication after one transaction
    return jsonify({"status": "success", "message": f"Successfully transferred ${amount} to {recipient}!"})

if __name__ == '__main__':
    app.run(debug=True)
