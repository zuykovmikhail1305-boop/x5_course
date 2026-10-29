def rules(city_dict, rate_dict):
    warm_clother = True if city_dict['temp_c'] < 16 else False
    expensive = True if rate_dict > 90 else False

    return {
        'warm_clother': warm_clother,
        'expensive': expensive
    }