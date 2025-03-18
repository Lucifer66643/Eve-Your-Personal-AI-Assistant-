import requests
import random
from speak import speak 

category_dict = {
    'art': ['art', 'painting', 'sculpture'],
    'attitude': ['attitude', 'mindset', 'approach'],
    'best': ['best', 'top', 'excellent'],
    'birthday': ['birthday', 'anniversary', 'celebration'],
    'car': ['car', 'automobile', 'vehicle'],
    'computers': ['computers', 'technology', 'IT'],
    'cool': ['cool', 'awesome', 'fantastic'],
    'courage': ['courage', 'bravery', 'valor'],
    'dating': ['dating', 'relationship', 'romance', 'romantic'],
    'design': ['design', 'plan', 'blueprint'],
    'dreams': ['dreams', 'aspirations', 'visions', 'aspirating'],
    'fitness': ['fitness', 'health', 'exercise'],
    'friendship': ['friendship', 'companionship', 'alliance'],
    'funny': ['funny', 'humor', 'comedy'],
    'good': ['good', 'positive', 'beneficial'],
    'happiness': ['happiness', 'joy', 'cheerful'],
    'health': ['health', 'wellness', 'fitness'],
    'inspirational': ['inspirational', 'motivation', 'encouragement'],
    'intelligence': ['intelligence', 'smart', 'knowledge', 'smartness'],
    'leadership': ['leadership', 'guidance', 'management'],
    'life': ['life', 'existence', 'living'],
    'love': ['love', 'affection', 'romance', 'romantic'],
    'marriage': ['marriage', 'union', 'wedding'],
    'money': ['money', 'finance', 'wealth'],
    'morning': ['morning', 'dawn', 'sunrise'],
    'success': ['success', 'achievement', 'victory']
}

def get_category_from_command(command):
    command = command.lower()
    for category, keywords in category_dict.items():
        if any(keyword in command for keyword in keywords):
            return category
    return None

def fetch_quote(category):
    api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
    response = requests.get(api_url, headers={'X-Api-Key': 'Aq20kbnwBdFkDdRYMfgnbg==1qBcL7NkbkLAmPoV'})
    if response.status_code == requests.codes.ok:
        quotes = response.json()
        if quotes:
            return quotes[0]['quote']
    return "Sorry, I couldn't fetch a quote for that category."

def main():
    spoken_command = "Tell me an inspirational quote"
    category = get_category_from_command(spoken_command)

    if category is None:
        category = random.choice(list(category_dict.keys()))
        speak(f"I couldn't determine the category, so here's a quote from the {category} category.")

    quote = fetch_quote(category)
    speak(quote)

if __name__ == "__main__":
    main()
