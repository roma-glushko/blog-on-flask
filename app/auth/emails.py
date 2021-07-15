from flask import render_template

from app.auth import bp
from app.emails import send_email
from app.models import User


def send_password_reset_email(user: User):
    token = user.get_reset_password_token()

    send_email('[Twitty] Reset Password Request',
               sender=bp.config['ADMIN_EMAILS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
