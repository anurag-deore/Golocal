from flask import render_template,Response,jsonify, url_for, flash, redirect, request, abort,json
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm,FilterForm
from flaskblog.models import User,Post
from PIL import Image
import secrets
import math
import os
from flask_login import login_user, current_user, logout_user, login_required

def rad(n):
    return n * math.pi / 180

def getdistance(p1,p2):
    R = 6378137
    dLat = rad(float(p2['lat']) - float(p1['lat']))
    dLong = rad(float(p2['lng']) - float(p1['lng']))
    a = math.sin(dLat / 2) * math.sin(dLat / 2) +math.cos(rad(float(p1['lat']))) * math.cos(rad(float(p2['lat']))) *math.sin(dLong / 2) * math.sin(dLong / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route("/home",methods=['GET','POST'])
def home():
    posts=[]
    p1={}
    p2={}
    if request.method == 'POST':
        posts.clear()
        p1.clear()
        p2.clear()
        p1['lat'],p1['lng']= str(current_user.location_latlng).split(",")
        data = request.form.get('sendskills')
        filters = data.split(',')
        for f in filters:
            search = "%{}%".format(f)
            p = User.query.filter(User.skills.like(search)).all();
            for k in p :
                l = k.serialize()
                # l['skills'] = l['skills'].split(",")
                p2['lat'],p2['lng']= str(k.location_latlng).split(",")
                l['distance']=getdistance(p1,p2) 
                if l not in posts: 
                    posts.append(l)
        return jsonify(posts)
    else:
        users = User.query.all()
        return render_template('home.html',posts=users)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, category=form.category.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please Login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        if form.location.data == '' or form.location.data == ' ' or  form.location_latlng.data == '':
            pass
        else:
            current_user.location = form.location.data
            current_user.location_latlng = form.location_latlng.data
            print(form.location_latlng.data,"done")
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.skills = form.skills.data
        db.session.commit()
        flash('Changes updated successfully !', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.skills.data = current_user.skills
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
                        

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, 
            location=form.location.data, 
            minsal=form.minsal.data, 
            maxsal=form.maxsal.data, 
            description=form.description.data, 
            author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)
@app.route("/post")
def post_id():
    return render_template('post.html')


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data 
        post.location = form.location.data 
        post.minsal = form.minsal.data 
        post.maxsal = form.maxsal.data 
        post.description = form.description.data 
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.location.data = post.location
        form.minsal.data = post.minsal
        form.maxsal.data = post.maxsal
        form.description.data = post.description
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    # page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())
    return render_template('user_posts.html', posts=posts, user=user)