import speech_recognition as sr
import pyautogui
import keyboard

def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return ""

def type_text(text):
    pyautogui.write(text)

def main():
    while True:
        if keyboard.is_pressed('ctrl+alt+s'):
            spoken_text = listen_to_speech()
            if spoken_text:
                type_text(spoken_text)

if __name__ == "__main__":
    main()