from processing.service import build_city_summary
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Сводка по городу")
    parser.add_argument("--city", required=True, help="Название города, например Moscow")
    parser.add_argument("--currency", default="USD", help="ISO-код валюты (по умолчанию USD)")
    parser.add_argument("--json", action="store_true", help="Вывести сводку в формате JSON")
    args = parser.parse_args()

    try:
        full_summary = build_city_summary(args.city, args.currency.upper())
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(4)

    if args.json:
        print(json.dumps(full_summary, ensure_ascii=False, indent=2))
        return

    print(f"Сводка по городу {full_summary['city']}:")
    print(f"Погода: {full_summary['weather']}")
    print(f"Курс валюты: {full_summary['rate']}")
    print(f"Тёплая одежда: {full_summary['rules']['warm_clother']}")
    print(f"Дорогой курс: {full_summary['rules']['expensive']}")

if __name__ == "__main__":
    main()
