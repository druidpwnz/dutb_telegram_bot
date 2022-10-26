import telebot
import re
import os
import shutil
from modules.ig_parsers import post_downloader, profile_content_downloader, hashtag_downloader
from modules.proxy_getter import get_free_proxy
from modules.cryptocurrency import get_info
from modules.open_weather import get_weather

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
/cryptocurrency - To show crypto price
/weather - To show current temperature
/proxy_getter - To get a proxy list file
/ig_post_downloader - To download instagram post
/ig_profile_downloader - To download all profile content
/ig_hashtag_downloader - To download last 10 hashtag posts""",
    )


@bot.message_handler(commands=["ig_post_downloader"])
def ig_post_downloader(message):
    sent_msg = bot.send_message(message.chat.id, "Enter post URL")
    # next step message call main_post_downloader function
    bot.register_next_step_handler(sent_msg, main_post_downloader_handler)


def main_post_downloader_handler(message):
    url = message.text
    if re.match(
        "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
        url,
    ):
        bot.send_message(
            message.chat.id,
            "Processing download. If it takes a long time, try again later",
        )
        if post_downloader(url):
            # need change to project path
            path = "/home/druiduser/Documents/dutb_telegram_bot/temp_ig"
            for file in os.listdir(path):
                if file.endswith(".jpg"):
                    file_path = f"{path}/{file}"
                    photo = open(file_path, "rb")
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                if file.endswith(".mp4"):
                    file_path = f"{path}/{file}"
                    video = open(file_path, "rb")
                    bot.send_video(message.chat.id, video)
                    video.close()
            shutil.rmtree(path)
        else:
            bot.send_message(
                message.chat.id, "An error occurred. Try again a bit later"
            )
    else:
        bot.send_message(message.chat.id, "Sorry, wrong URL. Try again")


@bot.message_handler(commands=["ig_profile_downloader"])
def ig_profile_photos_downloader(message):
    sent_msg = bot.send_message(message.chat.id, "Enter account name")
    bot.register_next_step_handler(sent_msg, main_profile_downloader_handler)


def main_profile_downloader_handler(message):
    account_name = message.text
    bot.send_message(message.chat.id, "Processing download. If it takes a long time, try again later")
    if profile_content_downloader(account_name):
        path = f"/home/druiduser/Documents/dutb_telegram_bot/{account_name}"
        for file in os.listdir(path):
            if file.endswith(".jpg"):
                file_path = f"{path}/{file}"
                photo = open(file_path, "rb")
                bot.send_photo(message.chat.id, photo)
                photo.close()
            if file.endswith(".mp4"):
                file_path = f"{path}/{file}"
                video = open(file_path, "rb")
                bot.send_video(message.chat.id, video)
                video.close()
        shutil.rmtree(path)
    else:
        bot.send_message(message.chat.id, "An error occurred. Try again a bit later")


@bot.message_handler(commands=["ig_hashtag_downloader"])
def ig_hashtag_downloader(message):
    sent_msg = bot.send_message(message.chat.id, "Enter hashtag name")
    bot.register_next_step_handler(sent_msg, main_hashtag_downloader_handler)


def main_hashtag_downloader_handler(message):
    hashtag = message.text
    bot.send_message(message.chat.id, "Processing download. If it takes a long time, try again later")
    if hashtag.startswith("#"):
        hashtag = hashtag.lstrip("#")
    if hashtag_downloader(hashtag):
        path = f"/home/druiduser/Documents/dutb_telegram_bot/{hashtag}"
        for file in os.listdir(path):
            if file.endswith(".jpg"):
                file_path = f"{path}/{file}"
                photo = open(file_path, "rb")
                bot.send_photo(message.chat.id, photo)
                photo.close()
            if file.endswith(".mp4"):
                file_path = f"{path}/{file}"
                video = open(file_path, "rb")
                bot.send_video(message.chat.id, video)
                video.close()
        shutil.rmtree(path)
    else:
        bot.send_message(message.chat.id, "An error occurred. Try again a bit later")


@bot.message_handler(commands=["proxy_getter"])
def proxy_getter(message):
    bot.send_message(message.chat.id, "Wait a minute. Generating proxy list")
    if get_free_proxy():
        file_path = "/home/druiduser/Documents/dutb_telegram_bot/proxy_list.txt"
        file = open(file_path, "r")
        bot.send_message(message.chat.id, "Youre proxy list file:")
        bot.send_document(message.chat.id, file)
        file.close()
        os.remove(file_path)
    else:
        bot.send_message(message.chat.id, "An error occurred. Try again a bit later")


@bot.message_handler(commands=["cryptocurrency"])
def cryptocurrency(message):
    btc, eth = get_info()
    bot.send_message(message.chat.id, f"BTC - {btc} USD\nETH - {eth} USD")


@bot.message_handler(commands=["weather"])
def weather(message):
    sent_msg = bot.send_message(message.chat.id, "Enter city name")
    bot.register_next_step_handler(sent_msg, main_weather_handler)


def main_weather_handler(message):
    city = message.text.lower()
    weather = get_weather(city)
    if weather != None:
        bot.send_message(message.chat.id , f"Current temperature in {weather}")
    else:
        bot.send_message(message.chat.id , "Wrong city name")


bot.infinity_polling()
