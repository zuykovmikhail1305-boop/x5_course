from processing.preprocessing import rules
from clients.weather import get_weather
from clients.rates import get_rate

def build_city_summary(city, cur = 'usd'):
    weather = get_weather(city)
    rate = get_rate(cur)
    rules_dict = rules(weather, rate) 

    return {
        'city': city,
        'weather': weather,
        'rate': rate,
        'rules': rules_dict
    }