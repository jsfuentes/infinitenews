import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def send_email_when_error () :
    smtp_server = "mail.privateemail.com"
    smtp_port = 587
    smtp_username = os.getenv("SMTP_USERNAME")
    print("smtp_username : ",smtp_username)
    smtp_password = os.getenv("SMTP_PASSWORD")
    print("smtp_password : ",smtp_password)

    sender = "hello@mimosa.so"
    recipient = "thomaschang7@gmail.com"
    subject = "(Urgent) Stream crashed!"
    body = "Stream is crashed and needs urgent repair."

    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP(smtp_server, smtp_port) as server : 
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, recipient, message)

    return