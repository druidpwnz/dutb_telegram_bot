import telebot
import re
import os
from ig_parsers import post_downloader

with open("auth.txt") as auth_file:
    token = auth_file.read()

bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=["start"])
def start(message):
    first_name = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f"Hello, {first_name}. Welcome to DUTB. See /help for all available commands",
    )


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(
        message.chat.id,
        """Available Commands:
/ig_post_downloader - To download instagram post""",
    )


@bot.message_handler(commands=["ig_post_downloader"])
def ig_post_downloader(message):
    sent_msg = bot.send_message(message.chat.id, "Enter post URL")
    # next step message call url function
    bot.register_next_step_handler(sent_msg, main_post_downloader_handler)


def main_post_downloader_handler(message):
    url = message.text
    if re.match(
        "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
        url,
    ):
        bot.send_message(
            message.chat.id,
            "Youre URL recieved. Processing download. If it takes a long time, try again later",
        )
        if post_downloader(url):
            # need change to project path
            path = "/home/druiduser/Documents/dutb_telegram_bot/temp_ig"
            os.chdir(path)
            for file in os.listdir():
                if file.endswith(".jpg"):
                    file_path = f"{path}/{file}"
                    photo = open(file_path, "rb")
                    bot.send_photo(message.chat.id, photo)
                    os.remove(file_path)
        else:
            bot.send_message(
                message.chat.id, "An error occurred. Try again a bit later"
            )
    else:
        bot.send_message(message.chat.id, "Sorry, wrong URL. Try again")


bot.infinity_polling()
