import time

import twilioHandler
import emailHandler
import mysql.connector
from mysql.connector import Error

class user():
    def __init__(self, username, password, email, email_password, phone_number):
        self.username = username
        self.password = password
        self.email = email
        self.email_password = email_password
        self.phone_number = phone_number
class old_messages():
    def __init__(self, sender, recipient, subject):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject

class texts():
    def __init__(self, target, subject, message):
        self.target = target
        self.subject = subject
        self.message = message

def main():
    users = []
    held_messages = []
    HOST = 'localhost'
    PORT = 3306
    DATABASE = 'emailtexter'
    USER = "root"
    PASSWORD = ''
    SOCKET= "C:/xampp/mysql/mysql.sock"
    held_body = ''
    held_sender = ''
    held_subject = ''

    try:
        connection = mysql.connector.connect(host=HOST,
                                             database=DATABASE,
                                             user=USER,
                                             password=PASSWORD)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            query = ("SELECT username, password, email, email_password, phone_number FROM userinfo WHERE on_switch = 'on'")
            cursor.execute(query)

            for userIn in cursor:
                username, password, email, email_password, phone_number = userIn
                users.append(user(username, password, email, email_password, phone_number))

            for userr in users:
                print(userr.email)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")



    while True:
        # Recieves texts
        target, text_subject, message, fromWho = twilioHandler.recieve_messages()

        # Handles sending emails from texts
        if target != '' and text_subject != '' and message != '' and fromWho != '':
            for userr in users:
                if userr.phone_number == fromWho:
                    emailHandler.send_email(target, text_subject, message, userr.email, userr.email_password)

        for userr in users:
            # Recieves emails
            emailBody, sender, subject = emailHandler.recieve_email(userr.email, userr.email_password)
            held_messages.append(old_messages(sender, userr, subject))

            #Sends as texts
            if held_messages[users.index(userr)].sender != sender and held_messages[users.index(userr)].recipient == userr and held_messages[users.index(userr)].subject != subject:
                print("Made it")
                #twilioHandler.send_text(emailBody, userr.phone_number, sender, subject)
                held_messages[users.index(userr)] = old_messages(sender, userr, subject)

        # waits to repeat
        time.sleep(15)


if __name__ == '__main__':
    main()

