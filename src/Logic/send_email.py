from datetime import datetime
from os import environ
import smtplib

# from dotenv import load_dotenv
# load_dotenv()


def sendmail(user_data: list) -> None:
    HOST = environ.get("host")
    PORT = int(environ.get("port"))
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()

    user_email = environ.get("user_email")
    password_email = environ.get("password_email")
    # print(user, password)
    server.login(user_email, password_email)

    subject, text = create_massage(user_data)
    from_addr = environ.get("from")
    to_addr = environ.get("to")
    
    header = f"From: {from_addr}\nTo: {to_addr}\nSubject: {subject}\n\n"
    msg = header + subject+"\n\n"+"\n".join(text)
    server.sendmail(from_addr, to_addr, msg.encode('utf-8'))
    server.close()


def create_massage(user_data: list) -> str:
    today = datetime.now()
    date = f"{today.year} / {today.month} / {today.day}"
    subject = "Error"
    text = f"Something goes wrong!\n\nTime: {date}"

    user_type = user_data[0]
    if user_type == "STARTUP":
        subject = "New sturtup apply"
        text = (f"Имя: {user_data[1]}",
                f"e-mail: {user_data[2]}",
                f"Идея: {user_data[3]}",
                f"Прототип: {user_data[4]}",
                f"Цель: {user_data[5]}",
                f"\nВремя: {date}")

    elif user_type == "MENTOR":
        subject = "New mentor apply"
        text = (f"Имя: {user_data[1]}",
                f"e-mail: {user_data[2]}",
                f"Компетенции: {user_data[3]}",
                f"Опыт: {user_data[4]}",
                f"Ссылки: {user_data[5]}",
                f"\nВремя: {date}")

    elif user_type == "PARTNER":
        subject = "New partner apply"
        text = (f"Имя: {user_data[1]}",
                f"e-mail: {user_data[2]}",
                f"Организация: {user_data[3]}",
                f"Должность: {user_data[4]}",
                f"\nВремя: {date}")
    return subject, text


if __name__ == "__main__":
    sendmail(["STARTUP", "test", "test", "test", "test", "test"])

    sendmail(["MENTOR", "test", "test", "test", "test", "test"])

    sendmail(["PARTNER", "test", "test", "test", "test", "test"])
    pass
