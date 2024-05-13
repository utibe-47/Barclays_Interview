from datetime import datetime
from datetime import timedelta

from sqlalchemy import desc, asc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer

from .config import Config
from ..thermos import db

tags = db.Table('bookmark_tag',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
                )


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship('Tag', secondary=tags, lazy='joined',
                            backref=db.backref('bookmarks', lazy='dynamic'))

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]
        else:
            self._tags = []

    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)


class TaskMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.now)
    task_id = db.Column(db.String)
    message = db.Column(db.String)
    signal = db.Column(db.String)
    user_id = db.Column(db.String)

    @staticmethod
    def newest(_time):
        return TaskMessage.query.order_by(asc('date')).filter(
            TaskMessage.date.between((datetime.now() - timedelta(0, _time)), datetime.now())).all()

    @staticmethod
    def all():
        return TaskMessage.query.all()


class FileSelection(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String, unique=True)
    file_name = db.Column(db.String, unique=True)

    @staticmethod
    def newest(num):
        return FileSelection.query.order_by(desc(FileSelection.date)).limit(num)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)
    primary_user = db.Column(db.Boolean)

    def get_reset_token(self, expires_sec=300):
        s = Serializer(Config.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def verify_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        else:
            return User.query.get(user_id)

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    def __repr__(self):
        return self.name
