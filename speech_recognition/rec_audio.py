import speech_recognition as sr
import pyaudio
from scipy.io.wavfile import write
from scipy.io import wavfile
import wavio as wv
import parselmouth
import wave
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def recorder():
    user_sound = "./speech_recognition/testrec.wav"
    #simply frequency
    freq = 44100


    # time to store data
    duration = 3

    # Start recorder with the given values of 
    # duration and sample frequency
    p = pyaudio.PyAudio()
    print('Recording')

    stream = p.open(format=pyaudio.paInt16, channels=2, rate=freq, frames_per_buffer=1024, input=True)

    frames = [] # Array pour stocker les trames

    # Store data in chunks for 3 seconds
    for i in range(0, int(freq / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(user_sound, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(freq)
    wf.writeframes(b''.join(frames))
    wf.close()

    return(user_sound)

def cutSignal():
        # On indique le fichier à traiter 
        TRESH = 200

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
            sound.export("recodedaudio.wav", format="wav")
            # On remplace la variable par le nouveau fichier mono
            file = "nostereo.wav"

        samplerate, data = wavfile.read(file)

        print(type(data))
        print(data[0])

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
                print(in_index)
                print(out_index)
                print(f"longueur du signal: {len(data)}" )
                print(len(data) + out_index)

        print(f"Moyenne du signal: {sum(data)/len(data)}")

        data_processed = data[int(in_index): len(data) + int(out_index)]
        plt.subplot(1 ,2, 1)
        plt.plot(data)
        plt.subplot(1 ,2, 2)
        plt.plot(data_processed)
        plt.show()

        scaled = np.int16(data_processed)
        wavfile.write("test.wav", samplerate, scaled)

def textRecogniser(file, word: str):


    r = sr.Recognizer()
    with sr.AudioFile(file) as src:
        r.adjust_for_ambient_noise(src)

        print("Say something !")
        audio = r.listen(src)

        print(" Recording now")

        try:
            text = r.recognize_google(audio, language="nl-NL")
            print(text)
            # if text == "hello world":
            #     print("success !")
            # else:
            #     print("Wrong answer !\n")
            #     print("Can try again")
            #     # main()
        except Exception as e:
            print("Error : " + str(e))

        #with open("recordertext.txt", "w") as file:
         #   file.write(text)


if __name__ == "__main__":
    # textRecogniser(recorder(), "Naam")
    recorder()
