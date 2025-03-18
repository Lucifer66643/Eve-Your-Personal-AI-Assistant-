import requests
from datetime import datetime
import speak

def get_weather():
    api_key = "841e8e8c0d614905bf8125914242006"
    city = "Pune"
    base_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        weather_data = response.json()

        location_name = weather_data.get("location", {}).get("name", "No location data")
        date = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('date', "No date data")
        temperature = weather_data.get("current", {}).get("temp_c", "No temperature data")
        condition = weather_data.get("current", {}).get("condition", {}).get("text", "No condition data")
        precip_mm = weather_data.get("current", {}).get("precip_mm", 0)
        feels_like = weather_data.get("current", {}).get("feelslike_c", 0)
        avg_temp = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('day', {}).get("avgtemp_c", 0)
        will_it_rain = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('day', {}).get("daily_will_it_rain", 0)
        sunrise = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('astro', {}).get('sunrise', "No sunrise data")
        sunset = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('astro', {}).get('sunset', "No sunset data")
        moonrise = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('astro', {}).get('moonrise', "No moonrise data")
        moonset = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('astro', {}).get('moonset', "No moonset data")
        moon_phase = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('astro', {}).get('moon_phase', "No moon phase data")
        daily_chance_of_rain = weather_data.get('forecast', {}).get('forecastday', [{}])[0].get('day', {}).get("daily_chance_of_rain", 0)

        weather_report = (
            f"The current temperature is {temperature}°C, but"
            f"feels like {feels_like}°C"
            f"Will it rain today? {'Yes' if will_it_rain else 'No'} with a {daily_chance_of_rain}% chance. "
        )

        print(weather_report)
        speak.speak(weather_report)

    except requests.RequestException as e:
        print(f"Error fetching weather data: {str(e)}")

def main():
    get_weather()
    while True:
        current_time = datetime.now().minute
        speak.speak.get_weather()
        continue

if __name__ == "__main__":
    main()