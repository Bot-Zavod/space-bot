from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from Logic.menu import main_menu, unknown_command
from Logic.language_set import language
from Logic.verification import *
from Logic.save_data import save_user 
from user_manager import UM, Startuper
from variables import *
import config as c


def startuper_final_q(update, context):
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


def startuper_why_we(update, context):
    lang = language(update)
    answer = update.message.text
    check = wdynp_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_why_we(answer)
        reply_keyboard = [[c.text['final_option'][lang], c.text['to_main_menu'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(text=c.text['startup_blank_q']['final_q'][lang].
                                  format(name=UM.currentUsers[update.effective_chat.id].get_name()),
                                  reply_markup=markup)
        
        return STARTUPER_FINAL_Q
    else:
        update.message.reply_text(text=c.text['errors']['why_we'][lang], 
                                        reply_markup=ReplyKeyboardRemove())
        return STARTUPER_WHY


def startuper_proto(update, context):
    lang = language(update)
    answer = update.message.text
    check = prototype_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_prototype(answer)
        update.message.reply_text(text=c.text['startup_blank_q']['why_we'][lang], reply_markup=ReplyKeyboardRemove())
        return STARTUPER_WHY
    else:
        update.message.reply_text(text=c.text['errors']['proto'][lang], reply_markup=ReplyKeyboardRemove())
        return STARTUPER_PROTO


def startuper_idea(update, context):
    lang = language(update)
    answer = update.message.text
    check = idea_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_idea(answer)
        update.message.reply_text(text=c.text['startup_blank_q']['proto'][lang], reply_markup=ReplyKeyboardRemove())
        return STARTUPER_PROTO
    else:
        update.message.reply_text(text=c.text['errors']['idea'][lang], reply_markup=ReplyKeyboardRemove())
        return STARTUPER_IDEA


def startuper_email(update, context):
    lang = language(update)
    answer = update.message.text
    check = email_check(answer)
    if check:
        UM.currentUsers[update.effective_chat.id].add_email(answer)
        update.message.reply_text(text=c.text['startup_blank_q']['idea'][lang], reply_markup=ReplyKeyboardRemove())
        return STARTUPER_IDEA
    else:
        update.message.reply_text(text=c.text['errors']['email'][lang], reply_markup=ReplyKeyboardRemove())
        return STARTUPER_EMAIL


def startuper_name(update, context): # not finished
    lang = language(update)
    answer = update.message.text
    check = name_check(answer)
    if check:
        UM.create_user(Startuper(update.effective_chat.id, answer.title(), 'startuper', update, context))
        update.message.reply_text(text=c.text['startup_blank_q']['email'][lang], reply_markup=ReplyKeyboardRemove())
        return STARTUPER_EMAIL
    else:
        update.message.reply_text(text=c.text['errors']['name'][lang], reply_markup=ReplyKeyboardRemove())
        return STARTUPER_NAME


### team, prototype and qualification round
def q_round_yes_no(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['yes'][lang]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['startup_ans']['fifth'][lang])
        update.message.reply_text(text=c.text['startup_blank_q']['name'][lang], reply_markup=ReplyKeyboardRemove())
        return STARTUPER_NAME ##################################### fill the blank
    elif answer == c.text['to_main_menu'][lang]:
        return main_menu(update, context)
    else:
        return unknown_command(update, context)


def team_yes_no(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['yes'][lang]:
        reply_keyboard = [[c.text['yes'][lang], c.text['to_main_menu'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(text=c.text['startup_q']['q_round'][lang], reply_markup=markup)
        return Q_ROUND_YES_NO
    elif answer == c.text['no'][lang]:
        reply_keyboard = [[c.text['to_main_menu'][lang], c.text['try_again'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text(text=c.text['startup_ans']['third'][lang], reply_markup=markup)
        return TRY_AGAIN_OR_MM # try again(go to question about tech) or move to main menu
    else:
        return unknown_command(update, context)


def proto_yes_no(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['yes'][lang]:
        reply_keyboard = [[c.text['yes'][lang], c.text['no'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
        update.message.reply_text(text=c.text['startup_q']['team'][lang], reply_markup=markup)
        return TEAM_YES_NO
    elif answer == c.text['no'][lang]:
        reply_keyboard = [[c.text['to_main_menu'][lang], c.text['try_again'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
        update.message.reply_text(text=c.text['startup_ans']['second'][lang], reply_markup=markup)
        return TRY_AGAIN_OR_MM
    else:
        return unknown_command(update, context)
### team, prototype and qualification round


### tech, edu and fantastic questions
def fantastic_yes_no(update, context): # if the answer to fantastic question is no, it means that the project is not
    lang = language(update) # related to the space at all
    answer = update.message.text
    if answer == c.text['yes'][lang]:
        reply_keyboard = [[c.text['yes'][lang], c.text['no'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
        update.message.reply_text(text=c.text['startup_q']['prototype'][lang], reply_markup=markup)
        return PROTOTYPE_YES_NO
    elif answer == c.text['no'][lang]:
        reply_keyboard = [[c.text['to_main_menu'][lang], c.text['try_again'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
        update.message.reply_text(text=c.text['startup_ans']['fourth'][lang], reply_markup=markup)
        return TRY_AGAIN_OR_MM
    else:
        return unknown_command(update, context)


def edu_yes_no(update, context):
    lang = language(update)
    answer = update.message.text
    if answer == c.text['yes'][lang]:
        reply_keyboard = [[c.text['yes'][lang], c.text['no'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
        update.message.reply_text(text=c.text['startup_q']['prototype'][lang], reply_markup=markup)
        return PROTOTYPE_YES_NO
    elif answer == c.text['no'][lang]:
        reply_keyboard = [[c.text['yes'][lang], c.text['no'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
        update.message.reply_text(text=c.text['startup_q']['fantastic'][lang], reply_markup=markup)
        return FANTASTIC_YES_NO
    else:
        return unknown_command(update, context)


def tech_yes_no(update, context): # takes the answer from tech_q(about tech question) and (if answer for tech_q is yes)
    lang = language(update)  # returns the answer for prototype question(yes or no) or (if answer for tech_q is no)
    answer = update.message.text  # returns the answer for education question
    if answer == c.text['yes'][lang] or answer == c.text['try_again'][lang]:
        reply_keyboard = [[c.text['yes'][lang], c.text['no'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
        update.message.reply_text(text=c.text['startup_q']['prototype'][lang], reply_markup=markup)
        return PROTOTYPE_YES_NO
    elif answer == c.text['no'][lang]:
        reply_keyboard = [[c.text['yes'][lang], c.text['no'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
        update.message.reply_text(text=c.text['startup_q']['edu'][lang], reply_markup=markup)
        return EDU_YES_NO
    else:
        return unknown_command(update, context)


def tech_q(update, context): #takes the answer from the prev question, if answer is 'let's go' - makes two buttons: yes
    lang = language(update) # or no, and sends the next question, then returns the answer of this question
    answer = update.message.text
    if answer == c.text['lets_go'][lang]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['startup_ans']['first'][lang])
        reply_keyboard = [[c.text['yes'][lang], c.text['no'][lang]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
        update.message.reply_text(text=c.text['startup_q']['tech'][lang], reply_markup=markup)
        return TECH_YES_NO
    elif answer == c.text['back'][lang]:
        return main_menu(update, context)
    else:
        return unknown_command(update, context)
### tech, edu and fantastic questions


def try_again_or_mm(update, context): # try again(go to question about tech) or move to main menu
    lang = language(update)
    answer = update.message.text
    if answer == c.text['try_again'][lang]:
        return tech_yes_no(update, context)
    elif answer == c.text['to_main_menu'][lang]:
        return main_menu(update, context)
    else:
        return unknown_command(update, context)


def startup(update, context):
    lang = language(update)
    reply_keyboard = [[c.text['lets_go'][lang], c.text['back'][lang]]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)#, one_time_keyboard=True)
    update.message.reply_text(text=c.text['bb_startup'][lang], reply_markup=markup)
    return TECH_OR_MM # goes to tech_q
