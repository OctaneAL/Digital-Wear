from api import db, app, login_manager
from api.forms import UserLogin, UserRegister, CreatePost, UpdateUser, UpdatePost
from api.models import Client, Product, ProductType
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, url_for, flash, request, send_from_directory
from PIL import Image
import io
import base64
import os
from .config import UPLOAD_FOLDER

bcrypt = Bcrypt(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))

@app.route('/')
def home():
    context = {
        'posts': Product.query.all()
    }
    return render_template("home.html", user = current_user, context = context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLogin()
    if form.validate_on_submit():
        user = Client.query.filter_by(email = form.email.data).first()
        flash('')
        if not user:
            flash("You have not been registered", category="error")
        else:
            if not Bcrypt.check_password_hash(bcrypt, user.password, form.password.data):
                flash("Wrong password", category="error")
            else:
                login_user(user, remember=True)
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
        new_product = Product(
            title = form.title.data,
            web_site = form.website.data,
            description = form.description.data,
            client_id = current_user.id,
        )
        db.session.add(new_product)
        db.session.commit()

        file = form.photo.data
        filename = str(new_product.id) + ".png"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        return redirect(url_for('profile')) 
    
    return render_template("addpost.html", form=form)

@app.route('/post/<int:id>')
def post(id):
    post = Product.query.filter_by(id=id).first()
    if post is None:
        return redirect(url_for("home"))
    context = {
        'title': post.title,
        'web_site': post.web_site,
        'description': post.description,
    }
    file_path = url_for('static', filename = "uploads/" + str(id) + ".png")
    return render_template('post.html', context=context, post = post, filename = file_path)



@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Product.query.get(post_id)

    if post.client_id != current_user.id:
        return redirect(url_for("home"))
    form = UpdatePost(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.website = form.website.data
        post.product_type_id = form.type.data
        db.session.merge(post)
        db.session.commit()
        return redirect(url_for('post', id=post.id))
    return render_template('update_post.html', title='Update Post', form=form, legend='Update Post', post_id = post_id)

@app.route("/post/<int:post_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Product.query.get(post_id)
    if post.client_id != current_user.id or post == None:
        return redirect(url_for("home"))
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(basedir, 'static/uploads/' + str(post_id) + '.png')
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('profile'))



@app.route('/profile')
@login_required
def profile():
    image = Client.query.get(current_user.id).photo
    if image != None:
        image = base64.b64encode(image).decode('utf-8')
    print(current_user.id)
    context = {
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'phone': current_user.phone,
        'description': current_user.description,
        'website': current_user.portfolio_url,
        'posts': Product.query.filter_by(client_id = current_user.id).all(),
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
