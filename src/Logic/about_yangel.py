from telegram import ReplyKeyboardMarkup

from Logic.menu import main_menu, unknown_command
from Logic.language_set import language
from variables import *
import config as c


def about_yangel(update, context):
    lang = language(update)
    reply_keyboard = [[c.text['first_menu']['first_option'][lang], c.text['first_menu']['second_option'][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(text=c.text['one_answer'][lang], reply_markup=markup)
    return ABOUT_YANGEL_HANDLER


def about_yangel_handler(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['first_menu']['first_option'][lang]:
        return main_menu(update, context)
    elif answer == c.text['first_menu']['second_option'][lang]:
        update.message.reply_text(text='http://yangelspace.tech')
    else:
        return unknown_command(update, context)
