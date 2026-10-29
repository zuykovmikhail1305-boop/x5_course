from clients.http import http_get



def get_rate(currency: str = "USD") -> float:
    resp = http_get(f"https://api.frankfurter.dev/v2/rate/{currency}/RUB", params=None)

    if resp.status_code in (404, 422):
        raise ValueError(f"Код валюты '{currency}' не найден")

    data = resp.json()

    rate = data.get("rate")
    if not isinstance(rate, (int, float)):
        raise ValueError("В ответе Frankfurter нет поля 'rate'")

    return float(rate)


if __name__ == "__main__":
    print(get_rate("USD"))
    print(get_rate("EUR"))
