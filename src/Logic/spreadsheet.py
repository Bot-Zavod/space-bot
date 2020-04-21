from oauth2client.service_account import ServiceAccountCredentials
import gspread

from random import choice
from datetime import datetime

"""
#to get all the values inside the file
sheet.get_all_values()

#to get exact row values in a second row (Since 1st row is the header)
sheet.row_values(2)

#to get all the column values in the column 'place'
sheet.col_values(16)

#to extract a particular cell value
sheet.cell(1, 1).value
"""


def spreadsheet(table, worksheet):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'Pandemia-parser-751d2a06ae54.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(table).get_worksheet(worksheet)
    return sheet


def random_fact():
    'Факты о космосе'
    worksheet = 0
    sheet = spreadsheet('Факты о космосе', worksheet)
    fact = choice(sheet.get_all_values())
    return fact[0]


def update_application(user_data):
    user_type = user_data[0]
    if user_type == "STARTUP":
        worksheet = 0
    elif user_type == "MENTOR":
        worksheet = 1
    elif user_type == "PARTNER":
        worksheet = 2
    sheet = spreadsheet('Заявки uasa_bot', worksheet)
    last_raw = len(sheet.get_all_values()) + 1
    today = datetime.now()
    date = f"{today.year}/{today.month}/{today.day}"
    raw = [date] + user_data[1:]
    sheet.insert_row(raw, last_raw)

    