from Logic.spreadsheet import update_application
from Logic.send_email import sendmail
from user_manager import UM
from database import DB


def save_user(chat_id: int) -> None:
    print(UM.currentUsers)
    user_data = UM.currentUsers[chat_id].get_data()

    # write to DB
    try:
        DB.update_user(chat_id, user_data[0])
    except:
        print("Failed to save user to DB")
    
    # write to GS
    try:
        update_application(user_data)
    except:
        print("Failed to save user to Spreedsheats")

    # send email
    try:
        sendmail(user_data)
    except:
        print("Failed to send email")

    UM.delete_user(chat_id)
