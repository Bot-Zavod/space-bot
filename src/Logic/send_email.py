from datetime import datetime
from os import environ
import smtplib


def sendmail(user_data):
    s = smtplib.SMTP()
    s.connect('email-smtp.eu-central-1.amazonaws.com', 587)
    s.starttls()

    user = environ.get("user_email")
    password = environ.get("password_email")
    print(user, password)
    s.login(user, password)

    today = datetime.now()
    date = f"{today.year} / {today.month} / {today.day}"
    subject = "Test"
    text = f"Something goes wrong!\n\nTime: {date}"

    user_type = user_data[0]
    if user_type == "STARTUP":
        subject = "New sturtup apply"
        text = f"Имя: {user_data[1]}\ne-mail: {user_data[2]}\nИдея: {user_data[3]}\nПрототип: {user_data[4]}\nЦель: {user_data[5]}\n\nВремя: {date}"
    elif user_type == "MENTOR":
        subject = "New mentor apply"
        text = f"Имя: {user_data[1]}\ne-mail: {user_data[2]}\nКомпетенции: {user_data[3]}\nОпыт: {user_data[4]}\nСсылки: {user_data[5]}\n\nВремя: {date}"
    elif user_type == "PARTNER":
        subject = "New partner apply"
        text = f"Имя: {user_data[1]}\ne-mail: {user_data[2]}\nОрганизация: {user_data[3]}\nДолжность: {user_data[4]}\n\nВремя: {date}"
    
    from_addr = "blach.smith.2000@gmail.com"
    to_addr = ""
    header = f"From: {from_addr}\nTo: {from_addr}\nSubject: {subject}\n\n"
    msg = header + text
    print(msg)
    s.sendmail(from_addr, from_addr, msg.encode('utf-8'))

# sendmail(["PARTNER", "1","2","3","4","5"])
