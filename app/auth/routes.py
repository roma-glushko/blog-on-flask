from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.emails import send_password_reset_email
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, \
    ResetPasswordForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))

    form = LoginForm()

    if not form.validate_on_submit():
        return render_template(
            'login.html',
            title='Sign In',
            form=form,
        )

    # tru to login the user

    user: User = User.query.filter_by(
        username=form.username.data
    ).first()

    if user is None or not user.check_password(form.password.data):
        flash('Invalid username or password')
        return redirect(url_for('auth.login'))

    login_user(user, remember=form.remember_me.data)

    next_page = request.args.get('next')

    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('posts.index')

    return redirect(next_page)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))

    form = RegistrationForm()

    if not form.validate_on_submit():
        return render_template('register.html', title='Register', form=form)

    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()

    flash('Congratulations, you are now a registered user!')

    return redirect(url_for('auth.login'))


@bp.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))

    form = ResetPasswordRequestForm()

    if not form.validate_on_submit():
        return render_template('reset_password_request.html',
                               title='Reset Password', form=form)

    user = User.query.filter_by(email=form.email.data).first()

    if user:
        send_password_reset_email(user)

    flash('Check your email for the instructions to reset your password')

    return redirect(url_for('auth.login'))


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))

    user: User = User.verify_reset_password_token(token)

    if not user:
        return redirect(url_for('posts.index'))

    form = ResetPasswordForm()

    if not form.validate_on_submit():
        return render_template('reset_password.html', form=form)

    user.set_password(form.password.data)
    db.session.commit()

    flash('Your password has been reset.')

    return redirect(url_for('auth.login'))
