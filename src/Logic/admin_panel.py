from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import csv
from datetime import datetime
from os import getcwd, remove

from Logic.menu import main_menu, unknown_command
from Logic.language_set import language
from Logic.spreadsheet import updateFact
from variables import *
from database import DB
#from Logic.stats_manager import Statistics
import Logic.graph_create
import subprocess
import config as c

push_text_notification = None # for text that admin wants to send


def stats_handler(update, context):
    # takes the data of users with applications sent
    date_data = DB.get_date('STARTUP', 'MENTOR', 'PARTNER')
    print(date_data)
    # writing the data from DB to csv file
    with open('datetime.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'specialization', 'startup', 'mentor', 'partner'])
        for z in date_data:
            writer.writerow([datetime.fromtimestamp(z[0]).date(), z[1]])
        file.close()
    path = getcwd() + "/src/Logic/graph_create.py"
    # launching second process to hold graph creation on the main thread
    subprocess.run(f'python3 {path}', shell=True)
    filename = getcwd() + '/graph.png'
    try:
        # reading the file with graph and sending to the admin
        with open(filename, 'rb') as file:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=file,
                                   caption='The graph')
        remove(filename)
    except FileNotFoundError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, there's still no submitted applications")


def push_handler(update, context, users_ids):
    global push_text_notification
    lang = language(update)
    for z in users_ids: # sending the notification message
        context.bot.send_message(chat_id=z, text=push_text_notification)
    user_number = len(users_ids)
    context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['push_success'][lang].format(user_number = user_number))
    return admin(update, context)


def push_who(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['options_admin']['all'][lang]:
        users_ids = DB.get_users()
        return push_handler(update, context, users_ids)
    elif answer == c.text['options_admin']['startup'][lang]:
        users_ids = DB.get_users('STARTUP')
        return push_handler(update, context, users_ids)
    elif answer == c.text['options_admin']['mentor'][lang]:
        users_ids = DB.get_users('MENTOR')
        return push_handler(update, context, users_ids)
    elif answer == c.text['options_admin']['partner'][lang]:
        users_ids = DB.get_users('PARTNER')
        return push_handler(update, context, users_ids)
    else:
        return unknown_command(update, context)


def push_text(update, context):
    global push_text_notification
    lang = language(update)
    push_text_notification = update.message.text
    reply_keyboard = [[c.text['options_admin']['all'][lang], c.text['options_admin']['startup'][lang]],
                      [c.text['options_admin']['mentor'][lang], c.text['options_admin']['partner'][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text=c.text['push_who_q'][lang], reply_markup=markup)
    return PUSH_WHO


def admin_handler(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['options_admin']['push'][lang]:
        update.message.reply_text(text=c.text['push_text_q'][lang], reply_markup=ReplyKeyboardRemove())
        return PUSH_TEXT
    elif answer == c.text['options_admin']['stats'][lang]:
        return stats_handler(update, context)
    elif answer == c.text['options_admin']['update'][lang]:
        facts = updateFact()
        msg = c.text['options_admin']['update_text'][lang]
        update.message.reply_text(msg.format(facts=facts), disable_web_page_preview=True)
    elif answer == c.text['to_main_menu'][lang]:
        return main_menu(update, context)
    else:
        return unknown_command(update, context)


def admin(update, context):
    lang = language(update)
    if update.message.chat.username in ('khmellevskyi', 'V_vargan'):
        reply_keyboard = [[c.text['options_admin']['push'][lang], c.text['options_admin']['stats'][lang]],
                          [c.text['options_admin']['update'][lang]],
                          [c.text['to_main_menu'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(text=c.text['hi_boss'][lang], reply_markup=markup)
        return ADMIN_HANDLER
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['sorry_not_boss'][lang])
