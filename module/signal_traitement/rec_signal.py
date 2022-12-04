# import sounddevice as sd
import pyaudio
from scipy.io.wavfile import write
from scipy.io import wavfile
from scipy.fft import rfft , rfftfreq, fftfreq, fft
import wavio as wv
import parselmouth
import sounddevice as sd
import wave
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns #bibliothèque Python de visualisation de données basée sur matplotlib
import math
import soundfile as sf
from PIL import Image, ImageChops
from pydub.silence import split_on_silence
from pydub import AudioSegment, effects 
from scipy.io.wavfile import read, write
import imagehash

class audio_traitement:

    def __init__(self):
        #simply frequency
        self.freq = 44100
        # time to store data
        self.__duration = 3
        self.__user_sound = 'user_sound.wav'
        self.ref_sound = 'user_sound_kabel.wav'
        self.audio = pyaudio.PyAudio()
        self.frames = [] # Array pour stocker les trames
        self.record(self.audio, self.freq , self.__duration, self.frames )
        data = self.save_record(self.audio, self.freq, self.frames, self.__user_sound)
        # samplerate, data = wavfile.read(self.__user_sound)
        efficace_data = self.efficace_value(data)
        moving_data = self.moving_average_of_2d_array(efficace_data)
        #print(moving_data)
        fft_data = self.fast_fourier_transform(moving_data)
        rms = self.rms_of_signal(moving_data)
        

        self.generate_graph(self.__user_sound , fft_data)
        #self.remove_silent()
        self.generate_Spectogram(self.__user_sound,self.ref_sound)


    def record(self,audio, freq, duration, frames):

        # Start recorder with the given values of
        # duration and sample frequency

        print('Recording')

        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=freq, frames_per_buffer=1024, input=True)

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
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(freq)
        wf.writeframes(b''.join(frames))
        wf.close()
        # TODO Trouver un moyen de génerer le graphique a partir des data initiale du son
        # Faire la moyenne sur les données
        # Refaire le graphique a partir des nouvelles données
        samplerate, data = wavfile.read(user_sound)
        return data


        try:
            with open('data.txt' ,  'w' , encoding='utf-8') as f:
                f.write(data)
        except:
            print("An exception occur")

        print( "sample rate" , samplerate , "longueur de data : "  , len(data) , 'data' , data)
        # moving_data = self.moving_average_of_2d_array(efficace_data)
        # fft_data = self.fast_fourier_transform(moving_data)


    def efficace_value(self , array):
        efficace_array = []
        # TODO Prendre chaque tableau dans la matrice et faire la valeur efficace
        # Voir comment faire la valeur efficace du tableau
        # for ind in range(len(array)):
            # efficace_array.append(np.sqrt(np.mean(np.array(array)**2)))

        efficace_array = abs(np.array(array))

        # print(efficace_array)

        return efficace_array


    def moving_average_of_2d_array(self, array, window=1000):
        array_average = []
        print(array)
        for ind in range(len(array) - window+1):
            array_average.append(np.mean(array[ind:ind+window]))

        print(f" leng == {len(array_average)}")
        print(array_average)
        return array_average

    def remove_silent (self, path):
        
        # Pass audio path
        rate, audio = read(path)
        # make the audio in pydub audio segment format
        aud = AudioSegment(audio.tobytes(),frame_rate = rate,
                     sample_width = audio.dtype.itemsize,channels = 1)
        # use split on sience method to split the audio based on the silence, 
        # here we can pass the min_silence_len as silent length threshold in ms and intensity thershold
        audio_chunks = split_on_silence(
            aud,
            min_silence_len = 100,
            silence_thresh = -45,
            keep_silence = 20,)
        #audio chunks are combined here
        audio_processed = sum(audio_chunks)
        audio_processed = np.array(audio_processed.get_array_of_samples())
        #Note the processed audio rate is not the same - it would be 1K
        return audio_processed, rate
    
    
    def generate_Spectogram(self , user_sound, ref_sound):
        #data, fs=sf.read(user_sound)
        #data_ref, fs_ref=sf.read(ref_sound)
        #sd.play(data, fs)
        #status = sd.wait()
        data_ref, fs_ref = self.remove_silent(ref_sound)
        data, fs = self.remove_silent(user_sound)
        plt.figure()
        #plt.subplot(1,2 , 1)
        plt.xlabel("time [s]")
        plt.ylabel("Frequency")
        plt.grid(visible=False)
        plt.title('Spectogram Recorded Audio')
        #plt.specgram(self.moving_average_of_2d_array, NFFT=128, Fs=1/3, noverlap=120, cmap='jet_r')Greys_r
        plt.specgram(data,Fs=fs, cmap='Greys_r')
        plt.savefig("image.png")
        plt.show()

        #plt.subplot(1,2 , 2)
        plt.xlabel("time [s]")
        plt.ylabel("Frequency")
        plt.grid(visible=False)
        #plt.specgram(self.moving_average_of_2d_array, NFFT=128, Fs=1/3, noverlap=120, cmap='jet_r')Greys_r
        plt.title('Spectogram Reference Audio')
        plt.specgram(data_ref,Fs=fs_ref, cmap='Greys_r')
        plt.savefig("image_ref.png")
        plt.show() # or plt.savefig("sound.png"), or plt.savefig("sound.pdf")
        
        i1 = Image.open("image.png").convert('RGB')
        print(i1.mode)
        i2 = Image.open("image_ref.png").convert('RGB')
        print(i2.mode)
        difference_0 = ImageChops.difference(i1,i2)
        print(difference_0.getbbox())
        difference_0.show()
       

        assert i1.mode == i2.mode, "Different kinds of images."
        assert i1.size == i2.size, "Different sizes."

        pairs = zip(i1.getdata(), i2.getdata())
        if len(i1.getbands()) == 1:
            #for gray-scale jpegs
            dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

        ncomponents = i1.size[0] * i1.size[1] * 3
        diff = (dif / 255.0 * 100) / ncomponents
        print ("Difference (percentage):", diff )

        
        cutoff = 3  # maximum bits that could be different between the hashes. 

        if diff < cutoff:
            print('images are similar')
        else:
            print('images are not similar')

            
    # recording = sd.rec(int(duration * freq), samplerate=freq,channels=2)

    # wf.wait()
    # sd.wait()

    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    # write("recording0.wav", freq, recording)

    # Convert the NumPy array to audio file
    # wv.write("recording1.wav", recording, freq, sampwidth=2)
    def generate_graph(self , user_sound , data):
        #print("Bonjour", data)
        sns.set()

        plt.rcParams['figure.dpi'] = 100 # Show nicely large images in this notebook
        snd = parselmouth.Sound(user_sound)

        # snd is all the user sound
        # need to elimate all the unused part of the sound
        # detect when the sound start and finish exactly (the time)

        # put all the value of the sound in an array
        snd_part = snd.extract_part(from_time=0, preserve_times=True)

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
        audio1='../../user_sound'
        plt.figure()
        plt.subplot(1,2 , 1)
        plt.plot(snd_part.xs(), snd_part.values.T)
        plt.xlim([snd_part.xmin, snd_part.xmax])
        plt.xlabel("time [s]")
        plt.ylabel("amplitude")
        # plt.axis([1.7, 2.5, -0.15 , 0.15])
        # plt.show() # or plt.savefig("sound.png"), or plt.savefig("sound.pdf")
        plt.subplot(1, 2, 2)
        print("data" , len(data))
        xf = rfftfreq((len(data)*2)-1, 1 / self.freq)
        plt.plot(xf , np.abs(data))
        
        plt.show()
        

    def moving_average_of_2d_array(self, array, window=3):
        array_average = []
        for ind in range(len(array) - window+1):
            array_average.append(np.mean(array[ind:ind+window]))
        return array_average

    def fast_fourier_transform(self, array):
        # fft = np.fft.fft(array)
        print(f"len array in fft {len(array)}")
        rfft_data = rfft(array)
        return rfft_data

    def rms_of_signal(self, array):
        rms = np.sqrt(np.mean(np.array(array)**2))
        return rms
