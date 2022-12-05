from scipy.io import wavfile
import matplotlib.pyplot as plt
import wave
import pyaudio
import numpy as np


TRESH = 200
DEBUG = False

def debug(param):
    if DEBUG:
        print(param)

# On indique le fichier à traiter 
file = "record.wav"

# On ouvre le fichier 
SPF = wave.open(file, "r")

# On vérifie que l'enregistrement est bien en mono
# Si pas on le passe du stéréo au mono  
if SPF.getnchannels() != 1:
    from pydub import AudioSegment
    sound = AudioSegment.from_wav(file)
    # On passe en mono 
    sound = sound.set_channels(1)
    # On exporte le fichier mono 
    sound.export("nostereo.wav", format="wav")
    # On remplace la variable par le nouveau fichier mono
    file = "nostereo.wav"

samplerate, data = wavfile.read(file)

debug(type(data))
debug(data[0])

in_index = 0
out_index = 0

for i in range(0, len(data)):
    if (data[i] > TRESH):
        in_index = i
        break
for o in range(0, len(data)):
    if (data[-o] > TRESH):
        out_index = -o
        break
debug(in_index)
debug(out_index)
debug(f"longueur du signal: {len(data)}" )
debug(len(data) + out_index)

debug(f"Moyenne du signal: {sum(data)/len(data)}")

data_processed = data[int(in_index): len(data) + int(out_index)]
plt.subplot(1 ,2, 1)
plt.plot(data)
plt.subplot(1 ,2, 2)
plt.plot(data_processed)
plt.show()

scaled = np.int16(data_processed)
wavfile.write("test.wav", samplerate, scaled)

