from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from Logic.menu import main_menu, unknown_command
from Logic.language_set import language
from Logic.save_data import save_user 
from Logic.verification import *

from user_manager import UM, Partner
from variables import *
import config as c


def partner_final_q(update, context):
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


def partner_email(update, context):
    lang = language(update)
    answer = update.message.text
    check = email_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_email(answer)
        reply_keyboard = [[c.text['final_option'][lang], c.text['to_main_menu'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text=c.text['partner_q']['final_q'][lang].
                                  format(name=UM.currentUsers[update.effective_chat.id].get_name()),
                                  reply_markup=markup)
        return PARTNER_FINAL_Q
    else:
        update.message.reply_text(text=c.text['errors']['email'][lang], reply_markup=ReplyKeyboardRemove())
        return PARTNER_EMAIL


def partner_org_pos(update, context):
    lang = language(update)
    answer = update.message.text
    check = position_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_organization_position(answer)
        update.message.reply_text(text=c.text['partner_q']['email'][lang], reply_markup=ReplyKeyboardRemove())
        return PARTNER_EMAIL
    else:
        update.message.reply_text(text=c.text['errors']['organization_position'][lang], reply_markup=ReplyKeyboardRemove())
        return PARTNER_ORG_POS


def partner_org_name(update, context):
    lang = language(update)
    answer = update.message.text
    check = name_organisation_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_organization_name(answer)
        update.message.reply_text(text=c.text['partner_q']['organization_position'][lang], reply_markup=ReplyKeyboardRemove())
        return PARTNER_ORG_POS
    else:
        update.message.reply_text(text=c.text['errors']['organization_name'][lang], reply_markup=ReplyKeyboardRemove())
        return PARTNER_ORG_NAME


def partner_name(update, context):
    lang = language(update)
    answer = update.message.text
    check = name_check(answer)
    if check:
        UM.create_user(Partner(update.effective_chat.id, answer.title(), 'partner', update, context))
        update.message.reply_text(text=c.text['partner_q']['organization_name'][lang], reply_markup=ReplyKeyboardRemove())
        return PARTNER_ORG_NAME
    else:
        update.message.reply_text(text=c.text['errors']['name'][lang], reply_markup=ReplyKeyboardRemove())
        return PARTNER_NAME


def partner_handler(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['partner_opt'][lang]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['partner_q']['answer'][lang])
        update.message.reply_text(text=c.text['partner_q']['name'][lang], reply_markup=ReplyKeyboardRemove())
        return PARTNER_NAME
    elif answer == c.text['to_main_menu'][lang]:
        return main_menu(update, context)
    else:
        return unknown_command(update, context)


def partner(update, context):
    lang = language(update)
    reply_keyboard = [[c.text['partner_opt'][lang], c.text['to_main_menu'][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text=c.text['partner'][lang], reply_markup=markup)
    return PARTNER_HANDLER
