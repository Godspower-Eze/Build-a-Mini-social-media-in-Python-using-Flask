from socialmedia import app, db
from flask import render_template, flash, redirect, url_for, request
from socialmedia.models import User, Post
from socialmedia.forms import PostCreationForm, UserCreationForm, LoginForm
from socialmedia import bcrypt
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
    post = Post.query.all()
    return render_template('home.html', post=post, title='Home')


@app.route('/createpost', methods=['GET', 'POST'])
def post_create():
    form = PostCreationForm()
    if form.validate_on_submit():
        post_title = form.post_title.data
        post_content = form.post_content.data
        create = Post(post_title=post_title, post_content=post_content, user_id=1)
        db.session.add(create)
        db.session.commit()
        flash('You have successfully created a new post', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='Create Post', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserCreationForm()
    if form.validate_on_submit():
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pasword)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully created an account. You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have logged in successfully', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid Credentials', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title=current_user.username + ' ' + 'Account')
