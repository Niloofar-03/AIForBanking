import speech_recognition as sr
import soundfile as sf
import numpy as np
import librosa

def record_voice_sample(filename="user_voice.wav"):
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Please say a phrase for authentication...")
        audio = recognizer.listen(source)

        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

    print(f"Voice sample saved as {filename}")

record_voice_sample()

import spacy
import speech_recognition as sr

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def parse_voice_command(command):
    doc = nlp(command)
    amount = None
    account = None
    
    # Extract amount and account type from the command
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            amount = ent.text
        elif ent.label_ == "ORG":
            account = ent.text
    
    return amount, account

def listen_for_command():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Please say your banking command...")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        print(f"Command received: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the command.")
        return None

def process_command():
    command = listen_for_command()  # Listen to user’s command
    if command:
        amount, account = parse_voice_command(command)  # Parse the command
        print(f"Amount: {amount}, Account: {account}")

# Example usage:
process_command()
@app.route('/authenticate-voice')
def authenticate_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    with open("user_sample.wav", "wb") as f:
        f.write(audio.get_wav_data())

    if compare_voices("user_sample.wav", "reference.wav"):
        session["authenticated"] = True
        return jsonify({"status": "success", "message": "Voice recognized!"})
    else:
        return jsonify({"status": "failure", "message": "Voice authentication failed."})
