from flask import Flask, render_template, jsonify, request, session
import speech_recognition as sr
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

AUTHORIZED_PHRASE = "My voice is my password"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/authenticate-voice')
def authenticate_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for authentication...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Recognized:", text)

        if text.lower() == AUTHORIZED_PHRASE.lower():
            session["authenticated"] = True  # Store in session
            return jsonify({"status": "success", "message": "Authentication successful!"})
        else:
            return jsonify({"status": "failure", "message": "Authentication failed! Try again."})

    except sr.UnknownValueError:
        return jsonify({"status": "error", "message": "Could not understand the audio"})
    except sr.RequestError:
        return jsonify({"status": "error", "message": "Check your internet connection"})

@app.route('/transfer', methods=['POST'])
def transfer_funds():
    if not session.get("authenticated"):
        return jsonify({"status": "failure", "message": "Authentication required!"})

    data = request.json
    amount = data.get("amount")
    recipient = data.get("recipient")

    if not amount or not recipient:
        return jsonify({"status": "error", "message": "Invalid transaction details"})

    # Reset authentication after one transaction
    session["authenticated"] = False

    return jsonify({"status": "success", "message": f"Transferred ${amount} to {recipient}!"})

if __name__ == '__main__':
    app.run(debug=True)
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import numpy as np

def compare_voices(sample_file, reference_file):
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
