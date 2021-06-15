import speech_recognition as sr

r = sr.Recognizer()
#speaker = pt.init()
#voices = speaker.getProperty("voices")
#speaker.setProperty("voice", voices[2].id)

class voice_search():

    def asist(self):
        try:
            with sr.Microphone() as source:
                print("listening...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source)
                com = r.recognize_google(audio)
                print(com)
                com = com.lower()
        except Exception as e:
            print("NOT RECOGNIZE", e)
            return "NOT RECOGNIZE"
        return com

