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

def textRecogniser(file, word: str):


    r = sr.Recognizer()
    with sr.AudioFile(file) as src:
        r.adjust_for_ambient_noise(src)

        print("Say something !")
        audio = r.listen(src)

        print(" Recording now")

        try:
            text = r.recognize_google(audio, language="nl-NL")
            print('Identified text:'+text)
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
