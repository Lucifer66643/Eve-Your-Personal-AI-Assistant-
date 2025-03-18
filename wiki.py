import wikipedia
import speak

def search_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        speak.speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak.speak(f"Disambiguation error: {e}")
    except wikipedia.exceptions.PageError as e:
        speak.speak(f"Page not found: {e}")