from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required

from app import db
from app.users.forms import EditProfileForm, FollowForm
from app.models import User, Post
from app.users import bp


@bp.before_request
def before_request():
    # todo: find more performant way to track last seen time

    if not current_user.is_authenticated:
        return

    current_user.last_seen = datetime.utcnow()
    db.session.commit()


@bp.route('/user/<username>')
@login_required
def user(username):
    follow_form = FollowForm()
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()) \
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('users.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('users.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'user.html',
        user=user,
        posts=posts.items,
        follow_form=follow_form,
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your changes have been saved.')

        return redirect(url_for('users.edit_profile'))

    if request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template(
        'edit_profile.html',
        title='Edit Profile',
        form=form,
    )


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = FollowForm()

    if not form.validate_on_submit():
        return redirect(url_for('posts.index'))

    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('posts.index'))

    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('users.user', username=username))

    current_user.follow(user)
    db.session.commit()

    flash('You are following {}!'.format(username))

    return redirect(url_for('users.user', username=username))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = FollowForm()

    if not form.validate_on_submit():
        return redirect(url_for('posts.index'))

    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('posts.index'))

    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('users.user', username=username))

    current_user.unfollow(user)
    db.session.commit()

    flash('You are not following {}.'.format(username))

    return redirect(url_for('users.user', username=username))
