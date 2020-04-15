from telegram import ReplyKeyboardMarkup

from Logic.menu import main_menu, unknown_command
from Logic.language_set import language
from variables import *
import config as c

from Logic.stats_manager import statistics


def get_stats(update, context):
    lang = language(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text=statistics.get_stats(lang))
    return more stat if person chooses


def admin_handler(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['options_admin']['push'][lang]:
        reply_keyboard = [[c.text['options_admin']['all'][lang], c.text['options_admin']['startup'][lang]],
                          [c.text['options_admin']['mentor'][lang], c.text['options_admin']['partner'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text=c.text['push_q'][lang], reply_markup=markup)
        pass #return PUSH_WHO, then PUSH_TEXT, PUSH_FINAL
    elif answer == c.text['options_admin']['stats'][lang]:
        return get_stats(update, context)
    elif answer == c.text['to_main_menu'][lang]:
        return main_menu(update, context)
    else:
        return unknown_command(update, context)


def admin(update, context):
    lang = language(update)
    if update.message.chat.username in ('khmellevskyi', 'V_vargan'):
        reply_keyboard = [[c.text['options_admin']['push'][lang], c.text['options_admin']['stats'][lang]],
                          [c.text['to_main_menu'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text=c.text['hi_boss'][lang], reply_markup=markup)
        return ADMIN_HANDLER
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['sorry_not_boss'][lang])
