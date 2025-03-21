import os
import random
from time import sleep
from dotenv import load_dotenv
import telebot

from config import GAME_LIST, HELLO_LIST, INFO_LIST, PLAYING_GIF

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHAT_BOT = telebot.TeleBot(API_KEY)


@CHAT_BOT.message_handler(commands=["start"])
def start(message):
    print("start called")
    CHAT_BOT.send_message(message.chat.id, "Send me any message!👾")
    print("\n")


@CHAT_BOT.message_handler(commands=["spam"])
def spam(message):
    print("spam called")
    for i in range(3):
        CHAT_BOT.send_message(message.chat.id, "spam!")
        sleep(3)


@CHAT_BOT.message_handler(content_types=["text"])
def handle_text(message):
    print("handle_text called")
    lower_text = message.text.lower()
    print("user input:", lower_text)

    if lower_text in HELLO_LIST:
        first_name = (
            message.chat.first_name if message.chat.first_name else "User"
        )
        CHAT_BOT.send_message(
            message.chat.id, f"Hello, {first_name}! How are you? 😊"
        )
    elif lower_text in INFO_LIST:
        # CHAT_BOT.send_message(
        #     message.chat.id, f"All chat info: {message.chat}"
        # )
        CHAT_BOT.send_message(message.chat.id, f"chat id: {message.chat.id}")
        CHAT_BOT.send_message(
            message.chat.id, f"username: {message.chat.username}"
        )
        CHAT_BOT.send_message(
            message.chat.id, f"user first name: {message.chat.first_name}"
        )
        CHAT_BOT.send_message(
            message.chat.id, f"user last name: {message.chat.last_name}"
        )
    elif lower_text in GAME_LIST:
        CHAT_BOT.send_message(message.chat.id, PLAYING_GIF)
        player_guess = CHAT_BOT.send_message(
            message.chat.id, "Guess 'heads' or 'tails': "
        )
        CHAT_BOT.register_next_step_handler(player_guess, flip_coin)
    else:
        CHAT_BOT.send_message(
            message.chat.id, "Sorry, I don't know this yet ;("
        )
    print("\n")


def flip_coin(message):
    print("flip_coin called")
    coin = random.choice(["heads", "tails"])
    lower_text = message.text.lower()
    chat_id = message.chat.id

    if lower_text == coin:
        return CHAT_BOT.send_message(chat_id, "You guessed correctly! 🎉")
    else:
        return CHAT_BOT.send_message(chat_id, "Sorry, you guessed wrong. 😬")


print("\nBot starting\n")
CHAT_BOT.polling(none_stop=True, interval=0)
print("\nBot stopped\n")
