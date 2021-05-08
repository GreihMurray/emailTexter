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

            query = ("SELECT * FROM userinfo")
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


    for i in range(0, 15):
        count = 0
        for userr in users:
            emailBody, sender, subject = emailHandler.recieve_email(userr.email, userr.email_password)
            held_messages.append(old_messages(sender, userr, subject))

            if held_messages[count].sender != sender and held_messages[users.index(userr)].recipient == userr and held_messages[users.index(userr)].subject != subject:
                print("Made it")
                #twilioHandler.send_text(emailBody, userr.phone_number, sender, subject)
                held_messages[users.index(userr)] = old_messages(sender, userr, subject)

            count += 1

        time.sleep(15)


if __name__ == '__main__':
    main()

