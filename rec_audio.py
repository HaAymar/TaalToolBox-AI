import speech_recognition as sr


def main():
    r = sr.Recognizer()
    with sr.Microphone() as src:
        r.adjust_for_ambient_noise(src)

        print("Say something !")
        audio = r.listen(src)

        print(" Recording now")

        try:
            text = r.recognize_google(audio)
            if text == "hello world":
                print("success !")
            else:
                print("Wrong answer !\n")
                print("Can try again")
                main()
        except Exception as e:
            print("Error : " + str(e))

        #with open("recordertext.txt", "w") as file:
         #   file.write(text)


if __name__ == "__main__":
    main()
