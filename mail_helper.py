import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import environ

# Required credentials for sending mail
USER = "893f96a5ee4e8c"
PASSWORD = environ["MAILPASS"]
HOST = "smtp.mailtrap.io"


def send_mail_mock(sender, receiver, html1, html2, subject):
    """
    Sends mock with two attached html elements
    :param sender: mail sender
    :param receiver: mail receiver
    :param html1: first html element
    :param html2: second html element
    :param subject: email subject
    """
    sender_email = sender
    receiver_email = receiver
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    # Create the plain-text and HTML version of your message
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(html1, "html")
    part2 = MIMEText(html2, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(HOST, 2525) as server:
        server.login(USER, PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())


def _run_as_standalone_script():
    """
    Tests script as the standalone
    """
    send_mail_mock(sender="my@gmail.com", receiver="rec@gmail.com", html1="", html2="", subject="Test")


if __name__ == "__main__":
    _run_as_standalone_script()
