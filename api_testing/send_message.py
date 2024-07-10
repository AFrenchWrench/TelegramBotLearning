from urllib import response
from message_update import update_messages
from decouple import config
import requests

def send_message(chat_ids, message):
    for chat_id in chat_ids:
        response = requests.get(f"https://api.telegram.org/bot{config("APItoken")}/sendMessage?chat_id={chat_id}&text={message}").json()
        print(response)

def main():
    messages = update_messages(config("APItoken"))["result"]

    chat_ids = set()

    for message in messages:
        chat_ids.add(
            message.get(list(message.keys())[1]).get("chat").get("id")
        )

    send_message(chat_ids, "Hello, this is a test message!")
if __name__=="__main__":
    main()

