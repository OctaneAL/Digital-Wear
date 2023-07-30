from api import db, app, login_manager
from api.forms import UserLogin, UserRegister, CreatePost, UpdateUser
from api.models import Client, Product
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, url_for, flash, request
from PIL import Image
import io
import base64

bcrypt = Bcrypt(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))

@app.route('/')
def home():
    return render_template("main.html", user = current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()
    if form.validate_on_submit():
        user = Client.query.filter_by(email = form.email.data).first()
        print(form.email.data)
        flash('')
        if not user:
            flash("You have not been registered", category="error")
        else:
            if not Bcrypt.check_password_hash(bcrypt, user.password, form.password.data):
                flash("Wrong password", category="error")
            else:
                rm = True if request.form.get("remember") else False
                login_user(user, remember=rm)
                return redirect(url_for('home')) 
    return render_template('login.html', form=form) 


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegister()
    if form.validate_on_submit():
        flash('')
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

@app.route('/log_out')
def log_out():
    logout_user()
    flash('')
    return redirect(url_for("login"))

@app.route('/add_post', methods = ['GET', 'POST'])
@login_required
def add_post():
    form = CreatePost()
    if form.validate_on_submit():
        flash('')
        print(form.title.data)
        print(form.description.data)
        new_product = Product(
            title = form.title.data,
            web_site = form.website.data,
            description = form.description.data,
            client_id = current_user.id,
        )
        db.session.add(new_product)
        db.session.commit()
        print('good')
        return redirect(url_for('profile')) 
    return render_template("addpost.html", form=form)

@app.route('/profile')
@login_required
def profile():
    image = Client.query.get(current_user.id).photo
    if image != None:
        image = base64.b64encode(image).decode('utf-8')

    context = {
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'phone': current_user.phone,
        'description': current_user.description,
        'website': current_user.portfolio_url,
    }
    return render_template("profile.html", context = context, image = image)

@app.route('/update', methods = ['GET', 'POST'])
@login_required
def update():
    user = Client.query.filter_by(id = current_user.id).first()
    form = UpdateUser(obj=user)
    if form.validate_on_submit() and request.method == 'POST':
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.description = form.description.data
        user.portfolio_url = form.website.data

        image = form.photo.data
        try:
            img = Image.open(image)
            img.thumbnail((528, 528))
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format='JPEG', optimize=True)
            img_data = img_byte_array.getvalue()
            user.photo = img_data
        except:
            pass

        db.session.merge(user)
        db.session.commit()
        user = Client.query.filter_by(id = current_user.id).first()
        return redirect(url_for('profile')) 
    
    return render_template("update.html", form = form)
