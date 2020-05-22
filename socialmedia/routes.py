from socialmedia import app, db
from flask import render_template, flash, redirect, url_for, request, abort
from socialmedia.models import User, Post
from socialmedia.forms import PostCreationForm, UserCreationForm, LoginForm, AccountInfo
from socialmedia import bcrypt
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
    post = Post.query.all()
    return render_template('home.html', post=post, title='Home')


@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def post_create():
    form = PostCreationForm()
    if form.validate_on_submit():
        post_title = form.post_title.data
        post_content = form.post_content.data
        create = Post(post_title=post_title, post_content=post_content, user_id=current_user.id)
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
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.get(current_user.id)
    form = AccountInfo()
    profile_image = url_for('static', filename='profile_image/' + current_user.profile_image)
    if request.method == 'POST':
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.bio = form.bio.data
        user.gender = form.gender.data
        user.email = form.email.data
        user.username = form.username.data
        db.session.commit()
        flash('You have successfully updated your profile', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.bio.data = user.bio
        form.gender.data = user.gender
        form.email.data = user.email
        form.username.data = user.username
    return render_template('account.html', title=current_user.username + ' ' + 'Account', profile_image=profile_image, form=form)


@app.route('/detail/<int:user_id>')
def detail_view(user_id):
    post_detail = Post.query.get_or_404(user_id)
    return render_template('detail.html', post_detail=post_detail)


@app.route('/detail/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostCreationForm()
    if post.author.id != current_user.id:
        abort(403)
    if request.method == 'POST':
        post.post_title = form.post_title.data
        post.post_content = form.post_content.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.post_title.data = post.post_title
        form.post_content.data = post.post_title
    return render_template('update.html', post=post, form=form)


@app.route('/detail/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You have deleted the post successfully', 'danger')
    return redirect(url_for('home'))
