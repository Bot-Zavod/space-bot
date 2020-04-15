from telegram.ext import Updater, Filters, ConversationHandler, MessageHandler, CommandHandler, Handler
from telegram import ReplyKeyboardMarkup #KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from os import environ as env, getcwd # for environmental variables
import logging #used for error detection

import config as c
from database import db
from user_manager import UM
from Logic.language_set import language, setting_lang
from variables import *
from Logic.menu import main_menu, unknown_command
from Logic.about_yangel import about_yangel, about_yangel_handler
from Logic.mentor import mentor, mentor_handler, mentor_name, mentor_expertise, \
                        mentor_experience, mentor_site, mentor_email, mentor_final_q
from Logic.partner import partner, partner_handler, partner_name, partner_org_name, \
                        partner_org_pos, partner_email, partner_final_q
from Logic.bb_startup import startup, tech_q, tech_yes_no, edu_yes_no, \
                        fantastic_yes_no, proto_yes_no, team_yes_no, \
                        q_round_yes_no, try_again_or_mm, startuper_name, \
                        startuper_email, startuper_idea, startuper_proto, \
                        startuper_why_we, startuper_final_q
from Logic.admin_panel import admin_handler, admin, get_stats, push_text, push_who
# from Logic.stats_manager import new_users_stats
from Logic.random_fact import random_fact

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main_menu_handler(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['main_menu']['first_option'][lang]:
        return about_yangel(update, context)
    elif answer == c.text['main_menu']['second_option'][lang]:
        return startup(update, context)
    elif answer == c.text['main_menu']['third_option'][lang]:
        return mentor(update, context)
    elif answer == c.text['main_menu']['fourth_option'][lang]:
        return partner(update, context)
    elif answer == c.text['main_menu']['fifth_option'][lang]:
        update.message.reply_text(text = random_fact())
    else:
        return unknown_command(update, context)


def start(update, context):
    """Welcome greating and proposing to choose the language"""
    lang = language(update)
    db.add_user(update.effective_chat.id)
    if update.effective_chat.id in UM.currentUsers:
        del UM.currentUsers[update.effective_chat.id]
    if lang == 1 or lang == 0:
        markup = ReplyKeyboardMarkup([[c.text['to_main_menu'][lang]]], resize_keyboard=True, one_time_keyboard=True)
        update.message.reply_text(text=c.text['welcome_back'][lang], reply_markup=markup)
        return MAIN_MENU
    else:
        return LANG


def done(update, context):
    #context.bot.send_message('Your message was not recognized')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    api_key = env.get('API_KEY')

    updater = Updater(token=api_key, use_context=True)
    dispatcher = updater.dispatcher

    necessary_handlers = [CommandHandler('start', start),
                          CommandHandler('stop', done),
                          CommandHandler('admin', admin)]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LANG:                 [*necessary_handlers, MessageHandler(Filters.text, setting_lang)],
            MAIN_MENU:            [*necessary_handlers, MessageHandler(Filters.text, main_menu)],
            MAIN_MENU_HANDLER:    [*necessary_handlers, MessageHandler(Filters.text, main_menu_handler)],
            ABOUT_YANGEL:         [*necessary_handlers, MessageHandler(Filters.text, about_yangel)],
            ABOUT_YANGEL_HANDLER: [*necessary_handlers, MessageHandler(Filters.text, about_yangel_handler)],
            STARTUP:              [*necessary_handlers, MessageHandler(Filters.text, startup)],
            TECH_OR_MM:           [*necessary_handlers, MessageHandler(Filters.text, tech_q)],
            TECH_YES_NO:          [*necessary_handlers, MessageHandler(Filters.text, tech_yes_no)],
            PROTOTYPE_YES_NO:     [*necessary_handlers, MessageHandler(Filters.text, proto_yes_no)],
            EDU_YES_NO:           [*necessary_handlers, MessageHandler(Filters.text, edu_yes_no)],
            TEAM_YES_NO:          [*necessary_handlers, MessageHandler(Filters.text, team_yes_no)],
            TRY_AGAIN_OR_MM:      [*necessary_handlers, MessageHandler(Filters.text, try_again_or_mm)],
            FANTASTIC_YES_NO:     [*necessary_handlers, MessageHandler(Filters.text, fantastic_yes_no)],
            Q_ROUND_YES_NO:       [*necessary_handlers, MessageHandler(Filters.text, q_round_yes_no)],
            STARTUPER_NAME:       [*necessary_handlers, MessageHandler(Filters.text, startuper_name)],
            STARTUPER_EMAIL:      [*necessary_handlers, MessageHandler(Filters.text, startuper_email)],
            STARTUPER_IDEA:       [*necessary_handlers, MessageHandler(Filters.text, startuper_idea),*necessary_handlers],
            STARTUPER_PROTO:      [*necessary_handlers, MessageHandler(Filters.text, startuper_proto)],
            STARTUPER_WHY:        [*necessary_handlers, MessageHandler(Filters.text, startuper_why_we)],
            STARTUPER_FINAL_Q:    [*necessary_handlers, MessageHandler(Filters.text, startuper_final_q)],
            MENTOR_HANDLER:       [*necessary_handlers, MessageHandler(Filters.text, mentor_handler)],
            MENTOR_NAME:          [*necessary_handlers, MessageHandler(Filters.text, mentor_name)],
            MENTOR_EXPERTISE:     [*necessary_handlers, MessageHandler(Filters.text, mentor_expertise)],
            MENTOR_EXPERIENCE:    [*necessary_handlers, MessageHandler(Filters.text, mentor_experience)],
            MENTOR_SITE:          [*necessary_handlers, MessageHandler(Filters.text, mentor_site)],
            MENTOR_EMAIL:         [*necessary_handlers, MessageHandler(Filters.text, mentor_email)],
            MENTOR_FINAL_Q:       [*necessary_handlers, MessageHandler(Filters.text, mentor_final_q)],
            PARTNER:              [*necessary_handlers, MessageHandler(Filters.text, partner)],
            PARTNER_HANDLER:      [*necessary_handlers, MessageHandler(Filters.text, partner_handler)],
            PARTNER_NAME:         [*necessary_handlers, MessageHandler(Filters.text, partner_name)],
            PARTNER_ORG_NAME:     [*necessary_handlers, MessageHandler(Filters.text, partner_org_name)],
            PARTNER_ORG_POS:      [*necessary_handlers, MessageHandler(Filters.text, partner_org_pos)],
            PARTNER_EMAIL:        [*necessary_handlers, MessageHandler(Filters.text, partner_email)],
            PARTNER_FINAL_Q:      [*necessary_handlers, MessageHandler(Filters.text, partner_final_q)],
            ADMIN_HANDLER:        [*necessary_handlers, MessageHandler(Filters.text, admin_handler)],
            GET_STATS:            [*necessary_handlers, MessageHandler(Filters.text, get_stats)],
            PUSH_TEXT:            [*necessary_handlers, MessageHandler(Filters.text, push_text)],
            PUSH_WHO:             [*necessary_handlers, MessageHandler(Filters.text, push_who)],

        },

        fallbacks=[CommandHandler('stop', done)], allow_reentry=True
    )
    dispatcher.add_handler(conv_handler)
    #dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
