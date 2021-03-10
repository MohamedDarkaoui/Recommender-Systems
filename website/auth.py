from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import views
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)



@auth.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST' and request.form.get('which-form') == "sign-in":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('views.home'))
    elif request.method == 'POST' and request.form.get('which-form') == "sign-up":
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConf = request.form.get('passwordConf')
        if password == passwordConf:
            user = User.query.filter_by(email=email).first()
            if not user:
                new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('auth.registration'))

    return render_template('registration.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.registration'))



