import time
import functools
import threading
from time import sleep
from telegram.ext import CallbackContext

from variables import *
from Logic.language_set import language
import config as c


class UserManager:

    def __init__(self):
        self.user_removal_time = 3600
        self.currentUsers = {}
        self.userthread = threading.Thread(target=self.__remove_old_users)
        self.userthread.start()

    def __remove_old_users(self):
        while True:
            sleep(self.user_removal_time)
            if self.currentUsers != {}:
                print('deleteCycle')
                print(self.currentUsers)
            users_to_send_and_delete = []
            for user in self.currentUsers.values():
                if time.time() - user.lastActivityTime > self.user_removal_time and user.get_last_item() is None:
                    update = user.update
                    context = user.context
                    UserManager.notificate_user(update, context)
                elif time.time() - user.lastActivityTime > self.user_removal_time and user.get_last_item() is not None:
                    users_to_send_and_delete.append(user.chat_id)
            for id in users_to_send_and_delete:
                #return send_data()   -  the func that takes the data and send it via email
                self.delete_user(id)
                print('deleting user')
    @staticmethod
    def notificate_user(update, context):
        lang = language(update)
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['timeout'][lang])

    def delete_user(self, chat_id):
        if chat_id in self.currentUsers:
            del self.currentUsers[chat_id]
        else:
            print(f'[WARNING]DELETING UNEXISTING USER {chat_id}')

    def create_user(self, user):
        self.currentUsers[user.chat_id] = user


    # Users stored in dictionary with keys as
    # Structure {
    #   user_id: User-class object
    # }


class User:
    def __init__(self, chat_id, name, specialization, update, context):
        self.chat_id = chat_id
        self.name = name
        self.specialization = specialization
        self.email = None
        self.update = update
        self.context = context
        self.lastActivityTime = time.time()

    def refresh_action(func):
        def wrapper_refresh_time(self, *args, **kwargs):
            self.update_time()
            value = func(self, *args, **kwargs)
            return value

        return wrapper_refresh_time

    def update_time(self):
        self.lastActivityTime = time.time()

    def get_name(self):
        n1, n2 = self.name.split()
        return n1

    @refresh_action
    def add_email(self, email):
        self.email = email
        return email


class Startuper(User):
    def __init__(self, chat_id, name, specialization, update, context):
        super().__init__(chat_id, name, specialization, update, context)
        self.idea = None
        self.prototype = None
        self.why_we = None

    def __repr__(self):
        return f'Startuper: Name & last name: {self.name}\nEmail: {self.email}\n' \
               f'Idea: {self.idea}\nPrototype: {self.prototype}\n' \
               f'Why needs an acceleration program: {self.why_we}\n'

    def refresh_action(func):
        return User.refresh_action(func)

    @refresh_action
    def add_idea(self, idea):
        self.idea = idea
        return idea

    @refresh_action
    def add_prototype(self, prototype):
        self.prototype = prototype
        return prototype

    @refresh_action
    def add_why_we(self, why_we):
        self.why_we = why_we
        return why_we

    def get_last_item(self):
        return self.why_we

    def get_data(self):
        data = ["STARTUP",
                self.name, 
                self.email, 
                self.idea, 
                self.prototype, 
                self.why_we]
        return data


class Mentor(User):
    def __init__(self, chat_id, name, specialization, update, context):
        super().__init__(chat_id, name, specialization, update, context)
        self.expertise = None
        self.experience = None
        self.site = None

    def __repr__(self):
        return f'Mentor: Name & last name: {self.name}\nEmail: {self.email}\n' \
               f'Site: {self.site}\nExpertise: {self.expertise}\nExperience: {self.experience}\n'

    def refresh_action(func):
        return User.refresh_action(func)

    @refresh_action
    def add_expertise(self, expertise):
        self.expertise = expertise
        return expertise

    @refresh_action
    def add_experience(self, experience):
        self.experience = experience
        return experience

    @refresh_action
    def add_site(self, site):
        self.site = site
        return site

    def get_last_item(self):
        return self.email

    def get_data(self):
        data = ["MENTOR",
                self.name, 
                self.email, 
                self.expertise,
                self.experience,
                self.site]
        return data


class Partner(User):
    def __init__(self, chat_id, name, specialization, update, context):
        super().__init__(chat_id, name, specialization, update, context)
        self.organization_name = None
        self.organization_position = None
        self.all_items = [self.name, self.email, self.organization_name, self.organization_position]

    def __repr__(self):
        return f'Partner: Name & last name: {self.name}\nEmail: {self.email}\n' \
               f'Organization: {self.organization_name}\nPosition there: {self.organization_position}\n'

    def refresh_action(func):
        return User.refresh_action(func)

    def get_all_items(self):
        return [self.name, self.email, self.organization_name, self.organization_position]

    @refresh_action
    def add_organization_name(self, organization_name):
        self.organization_name = organization_name
        return organization_name

    @refresh_action
    def add_organization_position(self, organization_position):
        self.organization_position = organization_position
        return organization_position

    def get_last_item(self):
        return self.email

    def get_data(self):
        data = ["PARTNER",
                self.name, 
                self.email, 
                self.organization_name,
                self.organization_position]
        return data

UM = UserManager()
# if __name__ == "__main__":
#     user = User(100500)
#     user.addQuestions([1,2,3,4,5])
#     user.addAnswer(1, 0)
#     print(user.answers)





