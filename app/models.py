import os

from .app import db, admin, login_manager
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from sqlalchemy.ext.hybrid import hybrid_property

from flask_admin.form.upload import FileUploadField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from wtforms import DateTimeField
from sqlalchemy.event import listens_for


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', cascade='all, delete', lazy='dynamic')
    likes = db.relationship('Like', backref='user', cascade='all, delete')

    def __repr__(self):
        return self.name

    @hybrid_property
    def password(self):
        return self.password_hash
        # raise AttributeError('Attribute is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def all_posts(self):
        posts = self.posts.order_by(Post.created_at.desc()).all()        
        return posts


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(128), index=True, nullable=False)
    photo = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    likes = db.relationship('Like', backref='post', cascade='all, delete-orphan', lazy='dynamic')
    search_keywords = db.relationship('KeyWord', backref='post', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'title: {self.title}'

    def like(self, user):
        if not self.is_liked(user):
            l = Like(post=self, user=user)
            db.session.add(l)
            db.session.commit()

    def is_liked(self, user):
        return self.likes.filter_by(user_id=user.id).first() is not None

    def unlike(self, user):
        if self.is_liked(user):
            l = self.likes.filter_by(user_id=user.id).first()
            db.session.delete(l)
            db.session.commit()

    def to_json(self):
        photo = f'\static\pictures\{self.photo}'
        post = {
            'id': self.id,
            'title': self.title,
            'photo': photo,
            'user_id': self.user_id,
            'likes': self.likes.count()
        }
        return post

    def is_own(self, user):
        if user == self.user:
            return True
        return False

class KeyWord(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer(), primary_key=True)
    keyword = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))

    def __repr__(self):
        return f'keyword->{self.keyword} post->{self.post}'

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'liked_by: {self.user.name}'



@listens_for(Post, 'after_delete')
def del_file(mapper, connection, target):
    if target.photo:
        try:
            os.remove(os.path.join('./app/static/pictures', target.photo))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass

class UserView(ModelView):
    form_columns = ("name", "password")
    extend_existing=True

class PostView(ModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'photo': FileUploadField,
        'created_at':DateTimeField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'photo': {
            'label': 'photo',
            'base_path': './app/static/pictures',
            'allow_overwrite': False
        }
    }
    
# admin views
admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(ModelView(KeyWord, db.session))
admin.add_view(FileAdmin('./app/static', '/static/', name='Static Files'))

# login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)