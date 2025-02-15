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
