from oauth2client.service_account import ServiceAccountCredentials
import gspread

from random import choice
from datetime import datetime
from os import path

from database import DB

"""
check this, in case you are not 
familiar with google spreadsheets

https://github.com/burnash/gspread
"""

json_creds = 'Vargan-API.json'
fullPathToCreds = path.abspath(
                path.expanduser(
                    path.expandvars(json_creds)))

def spreadsheet(table: str, worksheet: int) -> object:
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    print(fullPathToCreds)
    creds = ServiceAccountCredentials.from_json_keyfile_name(fullPathToCreds, scope)
    client = gspread.authorize(creds)

    sheet = client.open(table)
    sheet = client.open(table).get_worksheet(worksheet)
    return sheet


def updateFact():
    'Факты о космосе'
    worksheet = 0
    table = "Факты о космосе"
    sheet = spreadsheet(table, worksheet)
    facts = [tuple([fact[0]]) for fact in sheet.get_all_values()]
    DB.updateFacts(facts)

    return len(facts)


def update_application(user_data):
    user_type = user_data[0]
    worksheets = {"STARTUP":0, "MENTOR":1, "PARTNER":2}
    worksheet = worksheets[user_type]
    table = "Заявки uasa_bot"
    sheet = spreadsheet(table, worksheet)
    
    last_raw = len(sheet.get_all_values()) + 1
    today = datetime.now()
    date = f"{today.year}/{today.month}/{today.day}"
    raw = [date] + user_data[1:]
    sheet.insert_row(raw, last_raw)

if __name__=="__main__":
    # print(updateFact())
    pass

    