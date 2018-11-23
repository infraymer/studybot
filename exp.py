import telegram
from telegram import (InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler
import logging
import model

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

VIDEO, DESCRIPTION, TEST = range(3)


def startTask(bot, update):
    user = update.message.from_user
    logger.info("User of %s: started chat!", user.first_name)

    keyboard = [[InlineKeyboardButton("Поулчить текст", callback_data=str(VIDEO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('https://www.youtube.com/watch?v=l3fpeT7UUHg')
    update.message.reply_text('Hello! Task 1. Watch this is video, please ))', reply_markup=reply_markup)

    return VIDEO


def video(bot, update):
    # user = update.message.from_user
    # logger.info("User of %s is watched video", user.first_name)

    model.update_video_state(update)

    keyboard = [[InlineKeyboardButton("Пройти тест", callback_data=str(DESCRIPTION))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text='Perfect! It is cool man!)). \nВот тебе описание темы. Далее тебе нужно выполнить тест!',
        reply_markup=reply_markup
    )
    return DESCRIPTION


def description(bot, update):
    # user = update.message.from_user

    # logger.info("Description of %s: %s", user.first_name, 'user_photo.jpg')

    bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text='Погнали! Вопрос:\n Что тяжелее килограмм ваты или килограмм железа?'
    )

    return TEST


def test(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="/{}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def start(bot, update):
    model.add_user(update)
    user = update.message.from_user
    logger.info("User %s started dialog.", user.full_name)
    update.message.reply_text('Привет! Го проходить тест))\nДля этого отправь команду: /run')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("595069792:AAGnFK7tmzJYruORvHU00Dypu5AVMEEBz1k")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('run', startTask)],
        states={
            VIDEO: [CallbackQueryHandler(video)],
            DESCRIPTION: [CallbackQueryHandler(description)],
            TEST: [CallbackQueryHandler(test)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('start', start))

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
