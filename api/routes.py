from api import db, app, login_manager
from api.forms import UserLogin, UserRegister
from api.models import Client
from flask_bcrypt import Bcrypt
from flask_login import login_user
from flask import redirect, render_template, url_for

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()
    if form.validate_on_submit():
        user = Client.query.filter_by(email = form.email.data).first()
        if not user:
            pass # There is no user with this email, flash error
        else:
            if not Bcrypt.check_password_hash(user.password, form.password.data):
                pass # Wrong password, flash error
            else:
                login_user(user)
                return redirect(url_for('main')) 
    return render_template('login.html', form=form) 


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegister()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Client(
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            phone = form.phone.data,
            type = form.type.data,
            password = hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login')) 
    return render_template('register.html', form=form) 

@app.route('/')
def main():
    return render_template("base.html")