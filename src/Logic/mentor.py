from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from Logic.language_set import language
from Logic.menu import main_menu, unknown_command
from Logic.save_data import save_user 
from Logic.verification import *

from user_manager import UM, Mentor
from variables import *
import config as c


def mentor_final_q(update, context):
    lang = language(update)
    answer = update.message.text
    chat_id = update.effective_chat.id
    save_user(chat_id)
    if answer == c.text['final_option'][lang]:
        update.message.reply_text(text=c.text['final_answer'][lang])
        return main_menu(update, context)
    elif answer == c.text['to_main_menu'][lang]:
        return main_menu(update, context)
    else:
        return unknown_command(update, context)


def mentor_email(update, context):
    lang = language(update)
    answer = update.message.text
    check = email_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_email(answer)
        reply_keyboard = [[c.text['final_option'][lang], c.text['to_main_menu'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text=c.text['mentor_q']['final_q'][lang].
                                  format(name=UM.currentUsers[update.effective_chat.id].get_name()),
                                  reply_markup=markup)
        return MENTOR_FINAL_Q
    else:
        update.message.reply_text(text=c.text['errors']['email'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_EMAIL


def mentor_site(update, context):
    lang = language(update)
    answer = update.message.text
    check = site_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_site(answer)
        update.message.reply_text(text=c.text['mentor_q']['email'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_EMAIL
    else:
        update.message.reply_text(text=c.text['errors']['experience'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_SITE


def mentor_experience(update, context):
    lang = language(update)
    answer = update.message.text
    check = experience_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_experience(answer)
        update.message.reply_text(text=c.text['mentor_q']['site'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_SITE
    else:
        update.message.reply_text(text=c.text['errors']['experience'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_EXPERIENCE


def mentor_expertise(update, context):
    lang = language(update)
    answer = update.message.text
    check = expertise_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_expertise(answer)
        update.message.reply_text(text=c.text['mentor_q']['experience'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_EXPERIENCE
    else:
        update.message.reply_text(text=c.text['errors']['expertise'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_EXPERTISE


def mentor_name(update, context):
    lang = language(update)
    answer = update.message.text
    check = name_check(answer)
    if check:
        UM.create_user(Mentor(update.effective_chat.id, answer.title(), 'mentor', update, context))
        update.message.reply_text(text=c.text['mentor_q']['expertise'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_EXPERTISE
    else:
        update.message.reply_text(text=c.text['errors']['name'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_NAME


def mentor_handler(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['mentor_opt'][lang]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['mentor_q']['answer'][lang])
        update.message.reply_text(text=c.text['mentor_q']['name'][lang], reply_markup=ReplyKeyboardRemove())
        return MENTOR_NAME
    elif answer == c.text['back'][lang]:
        return main_menu(update, context)
    else:
        return unknown_command(update, context)


def mentor(update, context):
    lang = language(update)
    reply_keyboard = [[c.text['mentor_opt'][lang], c.text['back'][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text=c.text['mentor'][lang], reply_markup=markup)
    return MENTOR_HANDLER
