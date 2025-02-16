from flask import Flask, render_template, jsonify, request, session
import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import numpy as np

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session management
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

AUTHORIZED_PHRASE = "my word is my password"
REFERENCE_VOICE_FILE = "user_voice.wav"  # Ensure this file contains the correct secret phrase

def compare_voices(sample_file, reference_file):
    """Compare user voice sample with the reference voice."""
    sample_audio = AudioSegment.from_wav(sample_file)
    reference_audio = AudioSegment.from_wav(reference_file)

    sample_chunks = detect_nonsilent(sample_audio, min_silence_len=100, silence_thresh=-40)
    reference_chunks = detect_nonsilent(reference_audio, min_silence_len=100, silence_thresh=-40)

    if len(sample_chunks) == 0 or len(reference_chunks) == 0:
        return False  

    sample_length = np.mean([chunk[1] - chunk[0] for chunk in sample_chunks])
    reference_length = np.mean([chunk[1] - chunk[0] for chunk in reference_chunks])

    return abs(sample_length - reference_length) < 500

def record_voice_sample(filename="temp_voice.wav"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say the Secret Key for authentication...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

    print(f"User voice sample saved as {filename}")

@app.route('/')
def home():
    session["authenticated"] = False  # Reset authentication every time the page loads
    return render_template('index.html')

@app.route('/authenticate-voice', methods=['POST'])
def authenticate_voice():
    user_voice_file = "temp_voice.wav"
    record_voice_sample(user_voice_file)

    is_authenticated = compare_voices(user_voice_file, REFERENCE_VOICE_FILE)

    if is_authenticated:
        session["authenticated"] = True
        return jsonify({"status": "success", "message": "Authentication successful!"})
    else:
        return jsonify({"status": "failure", "message": "Authentication failed!"})

@app.route('/transfer', methods=['POST'])
def transfer_funds():
    """Handle secure bank transfers."""
    if not session.get("authenticated"):  
        return jsonify({"status": "failure", "message": "You must authenticate first."})

    data = request.json
    amount = data.get("amount")
    recipient = data.get("recipient")

    if not amount or not recipient:
        return jsonify({"status": "failure", "message": "Invalid transaction details."})

    session["authenticated"] = False  # Reset authentication after one transaction
    return jsonify({"status": "success", "message": f"Successfully transferred ${amount} to {recipient}!"})

if __name__ == '__main__':
    app.run(debug=True)
