import speech_recognition as sr


class speech_recognition : 
    def __init__(self):
        self.__recognizer = sr.Recognizer()
        self.audio = 0
        self.recording(self.__recognizer)
        
        
    def recording(self , recognizer):
        # r = sr.Recognizer()
        with sr.Microphone() as src:
            recognizer.adjust_for_ambient_noise(src)

            print("Say something !")
            self.audio = recognizer.listen(src)

            print(" Recording now")
            self.recognizer(recognizer)
    
    def recognizer(self, recognizer):
        try:
            text = recognizer.recognize_google(self.audio)
            if text == "hello world":
                print("success !")
            else:
                print("Wrong answer !\n")
                print("Can try again")
                self.recording(self.__recognizer)
        except Exception as e:
            print("Error : " + str(e))

        #with open("recordertext.txt", "w") as file:
        #   file.write(text)
