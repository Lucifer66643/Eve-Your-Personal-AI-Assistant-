import pyttsx3
import speech_recognition as sr

listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 135)

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text = "Hello, I am Yadnit."
    speak(text)
