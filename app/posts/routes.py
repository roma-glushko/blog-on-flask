from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required

from app import db
from app.posts.forms import PostForm
from app.models import Post
from app.posts import bp


@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('Your post is now live!')

        return redirect(url_for('posts.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False
    )

    next_url = url_for('posts.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('posts.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'index.html',
        title='Home Page',
        form=form,
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()) \
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)

    next_url = url_for('posts.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('posts.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template(
        'index.html',
        title='Explore',
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url,
    )