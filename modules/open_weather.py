import requests


def get_weather(city_name: str) -> str:
    api_key = "98ded0eb58f405049d2e75ee044f6616"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"
    response = requests.get(url=complete_url)
    data = response.json()
    try:
        temperature = data['main']['temp']
        return f"{city_name.capitalize()} {round(float(temperature), 1)}℃"
    except:
        print("Error weather")
    

if __name__ == "__main__":
    print(get_weather("Тернопіль"))
