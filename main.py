import os
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from brain import Eve1
import speak
import pyautogui
import wikipedia, window, weather, take_command, email, news, internetspeed as netspeed
from datetime import datetime, time
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import pdf_reader
import threading    
import home_automation

print(threading.enumerate())

# Start the Blynk connection in a separate thread
blynk_thread = threading.Thread(target=home_automation.run_blynk, daemon=True)
blynk_thread.start()

model = BertForSequenceClassification.from_pretrained('./intent_model')
tokenizer = BertTokenizer.from_pretrained('./intent_model')
model.eval()

# Function to predict intent
def predict_intent(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    
    predicted_label = torch.argmax(outputs.logits, axis=1).item()
    
    int_to_label = {
        0: "show_windows",
        1: "check_system_status",
        2: "close_window",
        3: "check_time",
        4: "check_internet_speed",
        5: "greet",
        6: "exit",
        7: "open_application",  # Ensure this matches your intent
        8: "search_wikipedia",
        9: "get_weather",
        10: "minimize_window",
        11: "maximize_window",
        12: "read_pdf",
        13: "control_appliance"
    }

    return int_to_label.get(predicted_label, None)  # Returns None if the intent is not found


def run_ai():
    try:
        speak.speak("How can I assist you today?")
        while True:
            command = take_command()
            
            if command:
                intent = predict_intent(command)
                
                if intent == False:
                    pass

                else:
                    if intent == "greet":
                        speak.speak("Hello, how can I assist you?")

                    elif intent == "exit":
                        speak.speak("Goodbye.")
                        break

                    elif intent == "open_application":
                        app_name = command.replace('open', "").strip()
                        speak.speak(f'Opening {app_name}')
                        pyautogui.press('super')
                        pyautogui.typewrite(app_name)
                        pyautogui.press('enter')

                    elif intent == "search_wikipedia":
                        query = command.replace('search', '').strip()
                        speak.speak(f'Searching Wikipedia for {query}')
                        wikipedia.search_wikipedia(query)

                    elif intent == "check_weather":
                        weather.get_weather()

                    elif intent == "internet_speed":
                        speak.speak("Checking internet speed")
                        speed = netspeed.SpeedTester()
                        result = speed.full_test
                        speak.speak(f"Download speed is {result['download']} Mbps and upload speed is {result['upload']} Mbps")

                    elif intent == "current_time":
                        current_time = datetime.now().strftime('%I:%M %p')
                        speak.speak(f'The current time is {current_time}')

                    elif intent == "control_device":
                        if "light" in command or "fan" in command or "tv" in command:
                            device = "light" if "light" in command else "fan" if "fan" in command else "tv"
                            action = "on" if "on" in command else "off"
                            home_automation.control_device(device, action)
                        else:
                            speak.speak("Please specify a device and an action.")
                    
                    elif intent == "check_system_status":
                        pass

                    elif intent  == "show_windows":
                        pass

                    elif intent == "close_window":
                        pass

            elif 'minimise window' in command:
                speak.speak('minimizening window')
                window.minimize_window()

            elif 'maximize window' in command:
                speak.speak('maximizening window')
                window.maximize_window()

            elif 'close' in command and 'DISPLAY' in os.environ:
                pyautogui.hotkey('alt', 'f4')
                speak.speak('Done, sir.')
               
            elif 'mute' in command:
                speak.speak('...')
                while True:
                    wake_up_command = take_command()
                    if 'unmute' in wake_up_command:
                        speak.speak("I am here sir")
                        break
                
            elif 'Analyse code' in command or 'start analyzing the code' in command:
                pass
                            
            elif 'read pdf ' in command or 'summarize the pdf ' in command or 'analyze the pdf ' in command:
                speak.speak('sir please provide the path of the book or pdf')
                file_path = input("Please enter the path to the PDF file: ")
                pdf_reader.pdf_reader(file_path)

            elif 'write an email' in command or 'compose an email' in command or 'send an email' in command:
                speak.speak('Sure sir, please provide the email address of the recipient.')
                receiver = input('Enter the email address: ')
                speak.speak('What should be the subject of the email?')
                subject = take_command()
                speak.speak('What should be the content of the email?')
                email_content = take_command()
                email.send_email(receiver, subject, email_content)
                speak.speak(f'Done, sir. Email sent successfully to {receiver}')

            elif "news" in command:
                news.NewsFromBBC()

            elif "Type for me in command" in command or "type" in command:
                pass

            else :
                prompt = command
                source = Eve1.generate(prompt, user_name = "Yadnit", web_access = False, stream = False )
                speak.speak(f'about this {prompt}')
                speak.speak(source)
                print(source)
                
    except KeyboardInterrupt:
        speak.speak("Goodbye, sir. It pleasure working with you.")

if __name__ == "__main__":
    speak.set_voice(12)
    run_ai()

def run_blynk():
    while True:
        try:
            blynk.run()  # Keep Blynk connection alive
        except Exception as e:
            print(f"Error in Blynk connection: {e}")
            time.sleep(5)  # Retry if there's an error ofc after a delay

