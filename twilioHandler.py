from twilio.rest import Client
from flask import Flask, request
from twilio import twiml


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACcf332a2e5e360c16e7458ed2b9b5eb3b'
auth_token = 'a7505f6652786f3da4338a4c6a7315e6'
client = Client(account_sid, auth_token)


def send_text(message, number, sender, subject):
    message = client.messages \
        .create(
             body="Email from: " + sender[0:100] + "\nsubject: " + subject[0:200] + "\nmessage: \n" + message[0:1000],
             from_='+15137177056',
             to='+'+number
         )

    print(message.sid)