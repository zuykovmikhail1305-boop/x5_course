from clients.http import http_get



def get_weather(city: str) -> dict:
    data = (http_get("https://geocoding-api.open-meteo.com/v1/search", params={"name": city, "count": 1})).json()

    if not data.get("results"):
        raise ValueError(f"Город '{city}' не найден")

    place = data["results"][0]
    lat = place.get("latitude")
    lon = place.get("longitude")
    if lat is None or lon is None:
        raise ValueError("В ответе геокодинга нет координат")

    forecast = (http_get("https://api.open-meteo.com/v1/forecast",
                                   params={"latitude": lat,
                                           "longitude": lon,
                                           "current": "temperature_2m,weather_code"})).json()

    current = forecast.get("current")
    if not isinstance(current, dict) or "temperature_2m" not in current or "weather_code" not in current:
        raise ValueError("В ответе прогноза нет полей temperature_2m и weather_code")

    temp = current["temperature_2m"]
    code = current["weather_code"]

    return {"city": city, "temp_c": temp, "code": code}


if __name__ == "__main__":
    print(get_weather('Moscow'))
