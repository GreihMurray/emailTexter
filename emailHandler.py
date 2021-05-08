import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import webbrowser
import os


class message():
    def __init__(self, subject, sender, body):
        self.subject = subject
        self.sender = sender
        self.body = body

# account credentials

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def send_email(target, subject, message, username, password):
    smtpObj = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    smtpObj.connect('smtp-mail.outlook.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()

    smtpObj.login(username, password)

    msg = MIMEMultipart()
    msg['From']=username
    msg['To']=target
    msg['Subject']=subject

    msg.attach(MIMEText(message, 'plain'))

    smtpObj.send_message(msg)

blank = 'blank'

last_message = message(blank, blank, blank)

def recieve_email(username, password):
    # number of top emails to fetch
    N = 1

    # create an IMAP4 class with SSL, use your email provider's IMAP server
    imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")
    # authenticate
    imap.login(username, password)

    # select a mailbox (in this case, the inbox mailbox)
    # use imap.list() to get the list of mailboxes
    status, messages = imap.select("INBOX")

    # total number of emails
    messages = int(messages[0])

    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)

                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments

                            print(body)
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        if last_message.body != body:
                            #print(body)
                            print(last_message.body)
                            # print only text email parts
                            #print("Subject:", subject)
                            #print("From:", From)
                            #print(body)

                print("="*100)

            last_message = message(subject, From, body)
    # close the connection and logout
    imap.close()
    imap.logout()

    return last_message.body, last_message.sender, last_message.subject
