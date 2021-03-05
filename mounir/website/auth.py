from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import views



auth = Blueprint('auth', __name__)



@auth.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST' and request.form.get('which-form') == "sign-in":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return redirect(url_for('views.home'))
    elif request.method == 'POST' and request.form.get('which-form') == "sign-up":
        print('signinup')
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConf = request.form.get('passwordConf')
        if password == passwordConf:
            user = User.query.filter_by(email=email).first()
            if not user:
                print('hi')
                new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('views.home'))
                    


    return render_template('registration.html')




