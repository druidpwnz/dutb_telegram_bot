import telebot
import re

with open("auth.txt") as auth_file:
    token = auth_file.read()

bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=["start"])
def start(message):
    # firstname of user
    first_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Hello, {first_name}. Welcome to DUTB. See /help for all available commands")


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
    bot.register_next_step_handler(sent_msg, url_handler)


def url_handler(message):
    url = message.text
    if re.match("^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$", url):
        bot.send_message(message.chat.id, "Youre URL recieved")
    else:
        bot.send_message(message.chat.id, "Sorry, wrong URL. Try again")


bot.infinity_polling()
