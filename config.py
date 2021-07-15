import os

basedir: str = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    POSTS_PER_PAGE = 10
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-secret-token-042'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
