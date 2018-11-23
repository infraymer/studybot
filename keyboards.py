from telegram import (InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton,
                      InlineKeyboardMarkup)
import telega


def remove():
    return ReplyKeyboardRemove()


def main_menu():
    keyboard = [['Вперед!']]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)


def run_test():
    # keyboard = [[InlineKeyboardButton(telega.CMD_START_STUDY, callback_data=telega.ACTION_TEST)]]
    # return InlineKeyboardMarkup(keyboard)
    keyboard = [['Пройти тест']]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)


def answer_variants(answers):
    buttons = []
    j = 0
    while j < len(answers):
        row = []
        for i in range(0, 2):
            if j < len(answers):
                row.append(InlineKeyboardButton(answers[j], callback_data=j))
                j += 1
        buttons.append(row)

    return InlineKeyboardMarkup(buttons)
