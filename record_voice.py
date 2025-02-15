import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration

print("Recording...")
audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)  # Use 1 channel (mono) instead of 2
sd.wait()  # Wait until recording is finished
write("reference.wav", fs, audio)
print("Saved as reference.wav")
