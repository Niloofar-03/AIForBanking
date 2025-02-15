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
