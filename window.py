import os
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import speak
import pyautogui
import webbrowser
import wikipedia, window, weather, take_command, email, news, internetspeed as netspeed
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Load the tokenizer and model from the saved directory
tokenizer = BertTokenizer.from_pretrained('./fine_tuned_model')
model = BertForSequenceClassification.from_pretrained('./fine_tuned_model', safe_serialization=True)

# Load dataset and fit label encoder
df = pd.read_csv('dataset.csv')
y = df['intent'].tolist()
le = LabelEncoder()
le.fit(y)

def predict_intent(command):
    """Predict the intent using the fine-tuned model."""
    encoding = tokenizer(command, return_tensors='pt', truncation=True, padding='max_length', max_length=32)
    with torch.no_grad():
        outputs = model(**encoding)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
    
    predicted_intent = le.inverse_transform([predicted_class])[0]
    
    return predicted_intent

def run_ai():
    try:
        speak.speak("How can I assist you today?")
        while True:
            command = take_command()
            
            if command:
                # Predict intent
                intent = predict_intent(command)
                
                if not intent:
                    speak.speak("Sorry, I couldn't understand your request.")
                else:
                    # Handle specific intents based on predictions
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

                    else:
                        speak.speak("Sorry, I couldn't match your request to any action.")

            # Other commands that don't rely on the intent prediction
            elif 'search' in command or 'search in wikipedia' in command:
                query = command.replace('search', '').strip()
                speak.speak('Searching for ' + query + ' on Wikipedia')
                wikipedia.search_wikipedia(query)

            elif 'minimize window' in command:
                speak.speak('Minimizing window')
                window.minimize_window()

            elif 'maximize window' in command:
                speak.speak('Maximizing window')
                window.maximize_window()

            elif 'show windows' in command:
                speak.speak('Showing open windows')
                window.print_window_details()

            elif 'switch to window' in command:
                speak.speak('Switching windows')
                window_title = command.replace('switch to window', '').strip()
                window.switch_to_window(window_title)

            elif 'system status' in command or 'check system status' in command:
                pass  # Add your system status logic here

            elif 'close' in command and 'DISPLAY' in os.environ:
                pyautogui.hotkey('alt', 'f4')
                speak.speak('Done, sir.')

            elif 'time' in command:
                current_time = datetime.now().strftime('%I:%M %p')
                speak.speak('Current time is ' + current_time)

            elif 'check internet speed' in command or 'internet speed' in command:
                speak.speak("Started diagnosis")
                speed = netspeed.SpeedTester()
                result = speed.full_test
                speak.speak("Diagnosis complete")
                speak.speak(result)
               
            elif 'sleep' in command:
                speak.speak('Okay sir, I am going to sleep. Wake me up by saying "wake up"!')
                while True:
                    wake_up_command = take_command()
                    if 'wake up' in wake_up_command:
                        speak.speak("I am awake now, sir!")
                        break
            
            elif 'mute' in command:
                while True:
                    mute_command = take_command()
                    if "unmute" in mute_command or 'speak' in mute_command:
                        speak.speak("Unmuted")

            elif 'analyze code' in command or 'start analyzing the code' in command:
                pass  # Add your code analysis logic here
                            
            elif 'read pdf' in command or 'summarize the pdf' in command or 'analyze the pdf' in command:
                speak.speak('Sir, please provide the path of the PDF.')
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

            elif 'todays weather' in command or 'weather' in command:
                weather.get_weather()

            elif "search on google" in command:
                query = command.replace('search on google', '').strip()
                speak.speak('Searching for ' + query + ' on Google')
                url = 'https://google.com/search?q=' + command.split('search on google')[1]
                try:
                    webbrowser.get().open(url)
                    speak.speak('This is what I found, sir.')
                except:
                    speak.speak('Please check your Internet connection.')

            elif "news" in command:
                news.NewsFromBBC()

            else:
                prompt = command
                source = eve1.generate(prompt, user_name="Yadnit", web_access=False, stream=False)
                speak.speak(f'About this {prompt}')
                speak.speak(source)
                print(source)
                
    except KeyboardInterrupt:
        speak.speak("Goodbye, sir. It was a pleasure working with you.")

if __name__ == "__main__":
    speak.set_voice(12)
    run_ai()
