# import sounddevice as sd
import pyaudio
from scipy.io.wavfile import write
from scipy.io import wavfile
import wavio as wv
import parselmouth
import wave
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class audio_traitement:

    def __init__(self):
        #simply frequency
        self.__freq = 44100
        # time to store data
        self.__duration = 5
        self.__user_sound = 'user_sound.wav'
        self.audio = pyaudio.PyAudio()
        self.frames = [] # Array pour stocker les trames
        self.record(self.audio, self.__freq , self.__duration, self.frames )
        self.save_record(self.audio, self.__freq, self.frames, self.__user_sound)
        self.generate_graph(self.__user_sound)


    def record(self,audio, freq, duration, frames):

        # Start recorder with the given values of
        # duration and sample frequency

        print('Recording')

        stream = audio.open(format=pyaudio.paInt16, channels=2, rate=freq, frames_per_buffer=1024, input=True)

        # Store data in chunks for 3 seconds
        for i in range(0, int(freq / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        audio.terminate()

    def save_record(self ,audio, freq, frames, user_sound):

        # Save the recorded data as a WAV file
        wf = wave.open(self.__user_sound, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(freq)
        wf.writeframes(b''.join(frames))
        wf.close()

        samplerate, data = wavfile.read(user_sound)


        try:
            with open('data.txt' ,  'w' , encoding='utf-8') as f:
                f.write(data)
        except:
            print("An exception occur")

        print( "sample rate" , samplerate , "longueur de data : "  , len(data), 'data' , data)

    # recording = sd.rec(int(duration * freq), samplerate=freq,channels=2)

    # wf.wait()
    # sd.wait()

    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    # write("recording0.wav", freq, recording)

    # Convert the NumPy array to audio file
    # wv.write("recording1.wav", recording, freq, sampwidth=2)
    def generate_graph(self , user_sound):
        sns.set()

        plt.rcParams['figure.dpi'] = 100 # Show nicely large images in this notebook
        snd = parselmouth.Sound(user_sound)

        # snd is all the user sound
        # need to elimate all the unused part of the sound
        # detect when the sound start and finish exactly (the time)

        # put all the value of the sound in an array
        snd_part = snd.extract_part(from_time=1.2, preserve_times=True)

        window = 4

        snd_list = []
        # snd_list.append(snd_part)

        # print(snd_list)
        # Object type: Sound
        # Object name: <no name>
        # Date: Wed Nov 30 11:00:42 2022

        # Number of channels: 2 (stereo)
        # Time domain:
        #    Start time: 1.2 seconds
        #    End time: 4.992290249433107 seconds
        #    Total duration: 3.7922902494331066 seconds
        # Time sampling:
        #    Number of samples: 167240
        #    Sampling period: 2.2675736961451248e-05 seconds
        #    Sampling frequency: 44100 Hz
        #    First sample centred at: 1.2000113378684807 seconds
        # Amplitude:
        #    Minimum: -0.079864502 Pascal
        #    Maximum: 0.105438232 Pascal
        #    Mean: 1.31748932e-06 Pascal
        #    Root-mean-square: 0.021210851 Pascal
        # Total energy: 0.00170615214 Pascal² sec (energy in air: 4.26538036e-06 Joule/m²)
        # Mean power (intensity) in air: 1.1247505e-06 Watt/m² = 60.51 dB
        # Standard deviation in channel 1: 0.0212109622 Pascal
        # Standard deviation in channel 2: 0.0212108666 Pascal

        # for ind in range(len(snd_part) - window+1):
        #     snd_part_average.append(np.mean(snd_part[ind:ind+window]))

        # print(snd_part_average)

        plt.figure()
        plt.plot(snd_part.xs(), snd_part.values.T)
        plt.xlim([snd_part.xmin, snd_part.xmax])
        plt.xlabel("time [s]")
        plt.ylabel("amplitude")
        plt.show() # or plt.savefig("sound.png"), or plt.savefig("sound.pdf")

    def moving_average_2d_array(self, array, window):
        # moving average
        array_average = []
        for ind in range(len(array) - window+1):
            array_average.append(np.mean(array[ind:ind+window]))
        return array_average

    def fast_fourier_transform(self, array):
        fft = np.fft.fft(array)
        return fft

    def rms_of_signal(self, array):
        rms = np.sqrt(np.mean(array**2))
        return rms
