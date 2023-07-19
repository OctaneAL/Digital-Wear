from api import db, app
from api.forms import UserLogin, UserRegister
from api.models import Client
from flask_bcrypt import Bcrypt
from flask_login import login_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()
    if form.validate_on_submit():
        user = Client.query.filter_by(email = form.email.data).first()
        if not user:
            pass # There is no user with this email, return error
        else:
            if not Bcrypt.check_password_hash(user.password, form.password.data):
                pass # Wrong password, return error
            else:
                login_user(user)
                return 'ddd' # temp solution
                return redirect(url_for('dashboard')) # final version
    return 'aaa' # temp solution
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST']) # final version
def register():
    form = UserRegister()

    if form.validate_on_submit():
        hashed_password = Bcrypt.generate_password_hash(form.password.data)
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
        return 'ccc' # temp solution
        return redirect(url_for('login')) # final version
    
    return 'bbb' # temp solution
    return render_template('register.html', form=form) # final version