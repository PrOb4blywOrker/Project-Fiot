from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():
    checked = 'checked_sign_up'
    return render_template('login.html', checked=checked)


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email_sign_up')
    name = request.form.get('user_sign_up')
    password = request.form.get('pass_sign_up')
    phone_sign_up = request.form.get('phone_sign_up')
    select_gender = request.form.get('select_gender')

    user = User.query.filter_by(email=email).first()

    if not user:

        new_user = User(email=email, name=name, password=password, phone=phone_sign_up, gender=select_gender)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))


@ auth.route('/login')
def login():
    checked = 'checked_sign_in'
    return render_template('login.html', checked=checked)


@ auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('user_log_in')
    password = request.form.get('pass_log_in')
    remember = True

    user = User.query.filter_by(name=name).first()
    if not user:
        return redirect('auth.login')

    if user.password == password:
        login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@ auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
