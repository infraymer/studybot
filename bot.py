import logging

from telegram.ext import (MessageHandler, Filters)
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import keyboards
import model
# Enable logging
import telega

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def message_handler(bot, update):
    user = update.message.from_user
    msg = update.message.text
    logger.info("User %s send message: %s", user.first_name, msg)
    state = model.User.get_state(user)

    if state in model.State.START and msg.lower() == telega.CMD_START_STUDY.lower():
        start_study_handler(bot, update)
    elif state in model.State.LESSON:
        lesson_handler(bot, update)
    elif state in model.State.QUESTION:
        question_handler(bot, update)
    elif state in model.State.ANSWER:
        answer_handler(bot, update)


def lesson_handler(bot, update):
    user = update.callback_query.from_user if update.message is None else update.message.from_user
    # user = update.message.from_user
    task, task_index = model.User.get_task(user)

    if task is None:
        bot.send_message(
            chat_id=user.id,
            text='Все задачи успешно выполнены!')
        return

    bot.send_message(
        chat_id=user.id,
        text='Задание №{}\n\n{}\n{}'.format(task_index + 1, task['description'], task['link']),
        reply_markup=keyboards.run_test()
    )
    model.User.set_state(user, model.State.QUESTION)


def answer_handler(bot, update):
    user = update.callback_query.from_user if update.message is None else update.message.from_user
    # user = update.message.from_user
    answ = update.message.text
    task = model.User.get_task(user)
    question, q_index = model.User.get_question(user)
    true_answer = question['true_answer']
    answers = question['answers']

    try:
        if len(answers) > 0:
            success = int(answ) - 1 == int(true_answer)
        else:
            success = true_answer.lower() == answ.lower()

        if success:
            bot.send_message(
                chat_id=user.id,
                text='Правильно!')
            model.User.next_question(user)
            model.User.set_state(user, model.State.QUESTION)
            question_handler(bot, update)
        else:
            bot.send_message(
                chat_id=user.id,
                text='Неверно!')
    except:
        bot.send_message(
            chat_id=user.id,
            text='Неверно!')


def question_handler(bot, update):
    user = update.callback_query.from_user if update.message is None else update.message.from_user
    task, task_index = model.User.get_task(user)
    question, q_index = model.User.get_question(user)

    if question is None:
        model.User.next_task(user)
        model.User.set_state(user, model.State.LESSON)
        lesson_handler(bot, update)
        return

    variants_text = ''
    answers = question['answers']

    if q_index == len(task['questions']):
        model.User.next_task(user)
        model.User.set_state(user, model.State.LESSON)
        lesson_handler(bot, update)
        return

    for i in range(0, len(answers)):
        variants_text += '{}. {}\n'.format(i + 1, answers[i])
    bot.send_message(
        chat_id=user.id,
        text=question['text'],
        reply_markup=keyboards.answer_variants(answers))
    model.User.set_state(user, model.State.ANSWER)
    # if len(task['question']) - 1 == q_index:
    #     return next_task_handler(bot, update)

    pass


def start_study_handler(bot, update):
    user = update.message.from_user
    model.User.set_state(user, model.State.LESSON)
    update.message.reply_text('Вперед за знаниями!')
    lesson_handler(bot, update)


def button(bot, update):
    query = update.callback_query

    user = query.from_user
    answ_index = query.data
    task = model.User.get_task(user)
    question, q_index = model.User.get_question(user)
    true_answer = question['true_answer']
    answers = question['answers']

    try:
        success = int(answ_index) == int(true_answer)

        if success:
            bot.send_message(
                text="Правильно!",
                chat_id=user.id)
            model.User.next_question(user)
            model.User.set_state(user, model.State.QUESTION)
            question_handler(bot, update)
        else:
            bot.send_message(
                text="Неверно!",
                chat_id=user.id)
    except Exception as err:
        bot.send_message(
            text="Неверно!",
            chat_id=user.id)


def start(bot, update):
    user = update.message.from_user
    model.add_user(user)
    logger.info("User %s started dialog.", user.first_name)
    update.message.reply_text(
        'Привет! Го проходить тест))\nДля этого отправь команду: Вперед!',
        reply_markup=keyboards.main_menu()
    )


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    REQUEST_KWARGS = {
        'proxy_url': telega.PROXY_URL,
        # Optional, if you need authentication:
        # 'username': 'PROXY_USER',
        # 'password': 'PROXY_PASS',
    }
    updater = Updater(telega.TOKEN)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, message_handler))
    dp.add_handler(CallbackQueryHandler(button))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logger.info('Bot RUNNING')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
