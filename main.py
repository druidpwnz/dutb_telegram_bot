from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to DUTB. See /help for all available commands")


def hello_world(update: Update, context: CallbackContext):
    update.message.reply_text("Hello World")


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Available Commands:
/hello_world - To get the Hello World message
    """
    )


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text
    )


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


def main():
    with open("auth.txt", "r") as auth_data:
        api_token = auth_data.read()
    updater = Updater(api_token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("hello_world", hello_world))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    # filters
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

    #start
    updater.start_polling()
    #stop from ctrl+c
    updater.idle()


if __name__ == "__main__":
    main()
