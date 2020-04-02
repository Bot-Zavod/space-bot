from telegram.ext import Updater, Filters, ConversationHandler, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup #KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from os import environ as env # for environmental variables
import logging #used for error detection
import config as c
from variables import *
from main_menu import main_menu
from language_set import language, setting_lang
from about_yangel import about_yangel, about_yangel_handler
from startup import startup, tech_q, tech_yes_no, edu_yes_no, fantastic_yes_no, proto_yes_no, team_yes_no, \
    q_round_yes_no, try_again_or_mm
from mentor import mentor, mentor_handler, mentor_name, mentor_expertise
from partner import partner, partner_handler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


### main menu
def main_menu_handler(update, context):
    lang = language()
    answer = update.message.text
    if answer == c.text['main_menu']['first_option'][lang]:
        return about_yangel(update, context)
    elif answer == c.text['main_menu']['second_option'][lang]:
        return startup(update, context)
    elif answer == c.text['main_menu']['third_option'][lang]:
        return mentor(update, context)
    elif answer == c.text['main_menu']['fourth_option'][lang]:
        return partner(update, context)
### main menu


def start(update, context):
    lang = language()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! I’m Maryna, Yangel Accelerator onboarding bot.')
    reply_keyboard = [[c.text['ua'], c.text['en']]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(text=c.text['ask_lang'], reply_markup=markup)
    return LANG


def done(update, context):
    update.message.reply_text('END')
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    api_key = env.get('API_KEY')

    updater = Updater(token=api_key, use_context=True)
    dispatcher = updater.dispatcher

    necessary_hendlers = [CommandHandler('start', start),
                          CommandHandler('stop', done)]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LANG: [MessageHandler(Filters.all, setting_lang), *necessary_hendlers],
            MAIN_MENU: [MessageHandler(Filters.all, main_menu), *necessary_hendlers],
            MAIN_MENU_HANDLER: [MessageHandler(Filters.all, main_menu_handler), *necessary_hendlers],
            ABOUT_YANGEL: [MessageHandler(Filters.all, about_yangel), *necessary_hendlers],
            ABOUT_YANGEL_HANDLER: [MessageHandler(Filters.all, about_yangel_handler), *necessary_hendlers],
            STARTUP: [MessageHandler(Filters.all, startup), *necessary_hendlers],
            TECH_OR_MM: [MessageHandler(Filters.all, tech_q), *necessary_hendlers],
            TECH_YES_NO: [MessageHandler(Filters.all, tech_yes_no), *necessary_hendlers],
            PROTOTYPE_YES_NO: [MessageHandler(Filters.text, proto_yes_no), *necessary_hendlers],
            EDU_YES_NO: [MessageHandler(Filters.text, edu_yes_no), *necessary_hendlers],
            TEAM_YES_NO: [MessageHandler(Filters.text, team_yes_no), *necessary_hendlers],
            TRY_AGAIN_OR_MM: [MessageHandler(Filters.text, try_again_or_mm), *necessary_hendlers],
            FANTASTIC_YES_NO: [MessageHandler(Filters.text, fantastic_yes_no), *necessary_hendlers],
            Q_ROUND_YES_NO: [MessageHandler(Filters.text, q_round_yes_no), *necessary_hendlers],
            STARTUPER_NAME: [],
            STARTUPER_EMAIL: [],
            STARTUPER_IDEA: [],
            STARTUPER_PROTO: [],
            STARTUPER_WHY: [],
            STARTUPER_FINAL_Q: [],
            STARTUPER_END: [],
            MENTOR_HANDLER: [MessageHandler(Filters.text, mentor_handler), *necessary_hendlers],
            MENTOR_NAME: [MessageHandler(Filters.text, mentor_name), *necessary_hendlers],
            MENTOR_EXPERTISE: [MessageHandler(Filters.text, mentor_expertise), *necessary_hendlers],
            MENTOR_EXPERIENCE: [],
            MENTOR_SITE: [],
            MENTOR_EMAIL: [],
            MENTOR_FINAL_Q: [],
            MENTOR_END: [],
            PARTNER: [MessageHandler(Filters.text, partner), *necessary_hendlers],
            PARTNER_HANDLER: [MessageHandler(Filters.text, partner_handler), *necessary_hendlers],

        },

        fallbacks=[CommandHandler('stop', done)]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
