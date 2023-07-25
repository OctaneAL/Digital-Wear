from api import db, app, login_manager
from api.forms import UserLogin, UserRegister
from api.models import Client
from flask_bcrypt import Bcrypt
from flask_login import login_user
from flask import redirect, render_template, url_for, flash

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))

@app.route('/')
def home():
    return render_template("base.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = Client.query.get(2)
    if user is not None:
        pass
    form = UserLogin()
    if form.validate_on_submit():
        user = Client.query.filter_by(email = form.email.data).first()
        if not user:
            flash("You have not been registered", category="error")
        else:
            if not Bcrypt.check_password_hash(bcrypt, user.password, form.password.data):
                flash("Wrong password", category="error")
            else:
                flash("You have been successfully logined", category="success")
                login_user(user)
                return redirect(url_for('home')) 
    return render_template('login.html', form=form) 


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegister()
    if form.validate_on_submit():
        user = Client.query.filter_by(email = form.email.data).first()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = Client(
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            phone = form.phone.data,
            client_type_id = form.type.data,
            password = hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login')) 

    return render_template('register.html', form=form) 

