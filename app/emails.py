from typing import List

from flask_mail import Message

from app import email


def send_email(subject: str, sender: str, recipients: List[str], text_body: str, html_body: str):
    msg = Message(subject, sender=sender, recipients=recipients)

    msg.body = text_body
    msg.html = html_body

    email.send(msg)
