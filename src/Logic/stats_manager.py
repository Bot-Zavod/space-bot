# import schedule
import time
import threading
import pandas as pd
from matplotlib import pyplot as plt

import config as c
from Logic.language_set import language


class Statistics:
    def __init__(self):
        self.graphthread = threading.Thread(target=self.__proccess)
        self.graphthread.start()

    def __proccess(self):
        date_df = pd.read_csv('datetime.csv')

        plt.hist(date_df['count'])
        plt.show()
        plt.savefig('graph.png', bbox_inches='tight')
'''
class Statistics:
    def __init__(self):
        #self.stats_dict = {}
        schedule.every().day.at('23:59').do(self.daily_procedure)
        schedule.every().sunday.at('23:59').do(self.weekly_procedure)
        self.statsthread = threading.Thread(target=self.__proccess)
        self.statsthread.start()

    def __proccess(self):
        while True:
            schedule.run_pending()
            time.sleep(20)

    def get_stats(self, lang):
        return (c.text['stats'][lang]).format(new_u_stats_daily=new_users_stats.daily,
                                              new_users_stats_weekly=new_users_stats.weekly,
                                              new_users_stats_monthly=new_users_stats.monthly)

    def get_more_stats(self, lang): # full stat(how many users used the bot,
        pass  #how many of them were near to start filling a blank, how many started filling and how many filled

    def daily_procedure(self):
        print('It happened')
        #self.stats_dict.clear()
        new_users_stats.last_day = new_users_stats.daily
        new_users_stats.daily = 0

    def weekly_procedure(self):
        new_users_stats.weekly = 0


class NewUsersStats(Statistics):
    def __init__(self):
        super().__init__()
        self.daily = 0
        self.weekly = 0
        self.monthly = 0
        self.last_day = 0
        self.lat_week = 0
        self.last_month = 0

    def add_stats(self, chat_id, username):
        self.daily += 1
        self.weekly += 1
        self.monthly += 1
        #if chat_id not in self.stats_dict:
            #self.stats_dict[chat_id] = username
        #elif chat_id in self.stats_dict:
            #pass


class StartupStats(Statistics):
    def __init__(self):
        super().__init__()
        self.near_start_daily = 0
        self.near_start_weekly = 0
        self.near_start_monthly = 0
        self.not_finished_daily = 0
        self.not_finished_weekly = 0
        self.not_finished_monthly = 0
        self.finished_daily = 0
        self.finished_weekly = 0
        self.finished_monthly = 0

    def add_stats(self):
        self.daily += 1
        self.weekly += 1
        self.monthly += 1


statistics = Statistics()
new_users_stats = NewUsersStats()
startup_users_stats = StartupStats()
'''
