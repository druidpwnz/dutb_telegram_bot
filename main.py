import telebot
import re
import os
import shutil
from modules.ig_parsers import (
    post_downloader,
    profile_content_downloader,
    hashtag_downloader,
)
from modules.proxy_getter import get_free_proxy
from modules.cryptocurrency import get_info
from modules.open_weather import get_weather
from modules.yt_downloader import yt_video_download, yt_audio_download

bot = telebot.TeleBot(token="API_TOKEN")

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
/cryptocurrency - Show cryptocurrency price
/weather - Show current weather
/youtube_video_downloader - Download video from youtube
/youtube_audio_downloader - Download audio from youtube
/ig_post_downloader - Download post from instagram (experimental)
/ig_profile_downloader - Download all posts from instagram profile (experimental)
/ig_hashtag_downloader - Download last 10 posts from instagram hashtag (experimental)
/proxy_getter - Get proxy list file""",
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
            path = "./cache"
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
    bot.send_message(
        message.chat.id, "Processing download. If it takes a long time, try again later"
    )
    if profile_content_downloader(account_name):
        path = f"./{account_name}"
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
    bot.send_message(
        message.chat.id, "Processing download. If it takes a long time, try again later"
    )
    if hashtag.startswith("#"):
        hashtag = hashtag.lstrip("#")
    if hashtag_downloader(hashtag):
        path = f"./cache"
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
        file_path = "./proxy_list.txt"
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
        bot.send_message(message.chat.id, f"Current temperature in {weather}")
    else:
        bot.send_message(message.chat.id, "Wrong city name")


@bot.message_handler(commands=["youtube_video_downloader"])
def youtube_video_downloader(message):
    sent_msg = bot.send_message(message.chat.id, "Enter URL")
    bot.register_next_step_handler(sent_msg, main_youtube_video_downloader_handler)


def main_youtube_video_downloader_handler(message):
    url = message.text
    if re.match(
        "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
        url,
    ):
        bot.send_message(
            message.chat.id,
            "Processing download. If it takes a long time, try again later",
        )
        if yt_video_download(url):
            path = "./cache"
            for file in os.listdir(path):
                if file.endswith(".mp4"):
                    file_path = f"{path}/{file}"
                    if os.path.getsize(file_path) < 52428800:
                        content = open(file_path, "rb")
                        bot.send_video(message.chat.id ,content)
                        content.close()
                    else:
                        bot.send_message(message.chat.id, "Sorry, the file is too large")
            shutil.rmtree(path)
        else:
            bot.send_message(
                message.chat.id, "An error occurred. Try again a bit later"
            )
    else:
        bot.send_message(message.chat.id, "Sorry, wrong URL. Try again")


@bot.message_handler(commands=["youtube_audio_downloader"])
def youtube_video_downloader(message):
    sent_msg = bot.send_message(message.chat.id, "Enter URL")
    bot.register_next_step_handler(sent_msg, main_youtube_audio_downloader_handler)


def main_youtube_audio_downloader_handler(message):
    url = message.text
    if re.match(
        "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
        url,
    ):
        bot.send_message(
            message.chat.id,
            "Processing download. If it takes a long time, try again later",
        )
        if yt_audio_download(url):
            path = "./cache"
            for file in os.listdir(path):
                if file.endswith(".mp4"):
                    file_path = f"{path}/{file}"
                    if os.path.getsize(file_path) < 52428800:
                        content = open(file_path, "rb")
                        bot.send_audio(message.chat.id ,content)
                        content.close()
                    else:
                        bot.send_message(message.chat.id, "Sorry, the file is too large")
            shutil.rmtree(path)
        else:
            bot.send_message(
                message.chat.id, "An error occurred. Try again a bit later"
            )
    else:
        bot.send_message(message.chat.id, "Sorry, wrong URL. Try again")


bot.infinity_polling()
