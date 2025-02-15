import speech_recognition as sr
from transaction import secure_transfer  # Import the transaction flow

# Initialize recognizer
recognizer = sr.Recognizer()

# Use microphone as source
with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        # If the recognized command includes 'transfer', trigger the secure transaction
        if "transfer" in text.lower():
            print("Initiating secure transfer...")
            secure_transfer()  # Call the secure transfer function from the transaction module

    except sr.UnknownValueError:
        print("Sorry, could not understand the audio")
    except sr.RequestError:
        print("Could not request results, check your internet connection")
import speech_recognition as sr

def record_user_voice(filename="user_voice.wav"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please say the phrase: 'My voice is my password' for authentication...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for the user's voice

        # Save the recorded audio to a WAV file
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())
    
    print(f"User voice sample saved as {filename}")

# Call this function to record the user's voice
record_user_voice("user_voice.wav")
import speech_recognition as sr

def record_reference_voice(filename="reference.wav"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please say the phrase: 'My voice is my password' for reference...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for the voice

        # Save the recorded reference audio to a WAV file
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

    print(f"Reference voice sample saved as {filename}")

# Call this function to record the reference voice
record_reference_voice("reference.wav")
