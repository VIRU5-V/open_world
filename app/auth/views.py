from flask import Blueprint, redirect, render_template, request, flash, redirect, url_for
from ..app import db
from ..models import User
from .forms import LoginForm, SignupForm
from flask_login import current_user, login_required, login_user, logout_user

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.user', username=current_user.name))
    if form.validate_on_submit() and request.method == 'POST':
        # get login form data
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        # login user if user exist
        user = User.query.filter_by(name=username).first()
        print(user)
        if user is not None and user.verify_password(password):
            login_user(user, remember=remember_me)
            flash(f'welcome back {current_user.name.upper()} 😍')
            return redirect(url_for('main_blueprint.user', username=user.name))
        flash('invalid username or password')
        
    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.posts'))
    form = SignupForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = User(
            name = username,
            password = password
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Welcome to Open_World! {user.name.upper()} 😎')
        return redirect(url_for('main_blueprint.user', username=user.name))
    return render_template('auth/signup.html', form=form)


@auth_blueprint.route('logout')
@login_required
def logout():
    flash(f'Open_World will be wating for you {current_user.name.upper()} 😊')
    logout_user()
    return redirect(url_for('main_blueprint.posts'))


# Ensure responses aren't cached
@auth_blueprint.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response