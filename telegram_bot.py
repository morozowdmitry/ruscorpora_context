import json
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from context import get_context

with open('token.json', 'r') as f:
    config = json.load(f)
    TOKEN = config['token']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def format_reply_message(lemma):
    context, source = get_context(lemma)
    return f"Ваш случайный контекст:\n\n{context}\n\nИсточник: {source}"


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Привет! '
        'Этот бот достаёт случайный контекст для заданного слова. '
        'Отправьте нормальную форму слова для получения контекста.'
    )


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Отправьте нормальную форму слова для получения контекста.')


def echo(update, context):
    """Echo the user message."""
    lemma = update.message.text
    echo_message = format_reply_message(lemma)
    update.message.reply_text(echo_message)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
