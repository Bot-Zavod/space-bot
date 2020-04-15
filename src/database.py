import sqlite3
import datetime
from os import getcwd
from datetime import datetime


class DbInterface:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def check_user(self, chat_id):
        sql = 'SELECT EXISTS(SELECT * from Users Where Chat_id = ?)'
        args = [chat_id]
        self.cursor.execute(sql, args)
        return True if self.cursor.fetchall()[0][0] == 1 else False

    def add_user(self, chat_id):
        sql = 'INSERT INTO Users (chat_id) VALUES (?)'
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.commit()
            print(f"User {chat_id} exists")

    def update_user(self, chat_id, status):
        sql = 'UPDATE Users SET status = (?), date = (?) WHERE chat_id = (?)'
        date = datetime.now().timestamp()
        args = [status, date, chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.commit()
            print(f"User {chat_id} couse fucking error")

    def get_date(self, status: str) -> list:
        sql = 'SELECT date from Users WHERE status = (?)'
        args = [status]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.commit()
            print("error to get datetime timestamp")
            
        timestamps = [i[0] for i in self.cursor.fetchall()]
        return timestamps

    def get_users(self, status = None) -> list:
        if not status:
            sql = 'SELECT chat_id from Users'
        else:
            sql = 'SELECT chat_id from Users WHERE status = (?)'
            args = [status]
        try:
            if not status:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.commit()
            print("error to get chat_id")

        users = [i[0] for i in self.cursor.fetchall()]
        return users


    # def clearUsers(self):
    #     sql = 'DELETE FROM USERS'
    #     try:
    #         self.cursor.execute(sql)
    #         self.conn.commit()
    #     except sqlite3.IntegrityError:
    #         print("ERROR")
    
    def idx(self): # creates unique indexes to make impossible to write the same chat_id in BD twi
        sql2 = 'CREATE UNIQUE INDEX idx_Language_chat_id ON Language (chat_id)'
        self.cursor.execute(sql2)

    def setLang(self, chat_id, lang):
        sql = 'INSERT OR REPLACE INTO Language (chat_id, lang) VALUES (?, ?)'
        args = [chat_id, lang]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("error")
            self.conn.commit()

    def getLang(self, chat_id):
        sql = 'SELECT EXISTS(SELECT * from Language Where chat_id = ?)'
        args = [chat_id]
        # print(chat_id)
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("error")
        if self.cursor.fetchall()[0][0] == 0:
            return None
        sql = 'SELECT lang from Language Where chat_id = ?'
        args = [chat_id]
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.commit()
            print("error")
        return self.cursor.fetchall()[0][0]

path = getcwd() + "/Space_DB.db"
DB = DbInterface(path)
# db = DbInterface(getcwd() + '/Space_DB.db')
# db.add_user(11)
# db.add_user(12)
# db.add_user(14)
# db.update_user(11, "new", 1.1)
# db.update_user(12, "new", 1.2)
# print(db.get_users("new"))
# print(checkUser(100))
# clearUsers()
