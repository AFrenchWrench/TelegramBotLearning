import requests
from decouple import config


def update_messages(token):
    response = requests.get(f"https://api.telegram.org/bot{token}/getUpdates").json()
    return response


def main():
    print(update_messages(config("APItoken")))


if __name__ == "__main__":
    main()
