from typing import List

from flask import render_template
from flask_mail import Message

from app import app, email
from app.models import User


def send_email(subject: str, sender: str, recipients: List[str], text_body: str, html_body: str):
    msg = Message(subject, sender=sender, recipients=recipients)

    msg.body = text_body
    msg.html = html_body

    email.send(msg)


def send_password_reset_email(user: User):
    token = user.get_reset_password_token()

    send_email('[Twitty] Reset Password Request',
               sender=app.config['ADMIN_EMAILS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
