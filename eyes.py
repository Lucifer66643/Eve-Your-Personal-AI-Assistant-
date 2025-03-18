import requests
import wikipedia
import speak

api_key = 'acc_a2b9dc3c82a80f2'
api_secret = '2dfc815d1161a5359900b9ba150daa36'

def get_top_tag(image_url=None, image_path=None):
    if image_url:
        response = requests.get(
            f'https://api.imagga.com/v2/tags?image_url={image_url}',
            auth=(api_key, api_secret)
        )
    elif image_path:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                'https://api.imagga.com/v2/tags',
                files={'image': image_file},
                auth=(api_key, api_secret)
            )
    else:
        raise speak.speak("Either image_url or image_path must be provided.")
    try:
        data = response.json()
    except ValueError:
        print("Response content is not valid JSON.")
        return None
    tags = data.get('result', {}).get('tags', [])
    if tags:
        top_tag = max(tags, key=lambda tag: tag['confidence'])
        object_name = top_tag['tag']['en']
        return object_name
    else:
        speak.speak("No tags found in the response.")
        return None, None

def main():
    image_url = None
    image_path = "/home/yadnitkale/projects/eve/download.jpeg"

    object_name = get_top_tag(image_url=image_url, image_path=image_path)

    if object_name:
        speak.speak(f"its a {object_name} sir")
        try:
            summary = wikipedia.summary(object_name, sentences=1)
            speak.speak(f"{summary}")
        except wikipedia.exceptions.PageError:
            print(f"No Wikipedia page found for {object_name}")
    else:
        print("No object detected.")

if __name__ == "__main__":
    main()
