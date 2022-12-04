from module.speech_recognition.rec_audio import speech_recognition
from module.signal_traitement.rec_signal import audio_traitement
# from module.test_signal.signal_test import signal_test

# valeur (racine carre de la somme de carre / par la s)
if __name__ == '__main__':
    # Signal Traitement
    audio_traitement()

    # Speech Recognition
    #print(speech_recognition("./speech_recognition/test/test-set/set1/rec1.wav", "mijn naam").getPrononciation())
    print(speech_recognition("./user_sound.wav", "kabel").getPrononciation())

    #Class servant de test pour le signal

    # signal_test()

