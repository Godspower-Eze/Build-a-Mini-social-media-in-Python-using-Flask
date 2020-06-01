from flask import request, render_template, redirect, Blueprint, url_for, flash
from flask_login import current_user, login_required, logout_user, login_user
from socialmedia import db
from socialmedia.models import Post, User
from .forms import (UserCreationForm,
                    LoginForm,
                    AccountInfo,
                    RequestChangePassword,
                    ChangePasswordFormFromToken)
from socialmedia import bcrypt
from .utils import send_reset_token, save_picture

users = Blueprint('users', __name__)


@users.route('/user_posts/<string:username>', methods=['GET', 'POST'])
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=1)
    return render_template('user.html', title=f"{user.username} Posts", posts=posts, user=user)


@users.route('/register', methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = UserCreationForm()
    if form.validate_on_submit():
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pasword)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully created an account. You can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.get(current_user.id)
    form = AccountInfo()
    profile_image = url_for('static', filename='profile_image/' + current_user.profile_image)
    if form.profile_image.data:
        picture_file = save_picture(form.profile_image.data)
        current_user.profile_image = picture_file

    if request.method == 'POST':
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.bio = form.bio.data
        user.gender = form.gender.data
        user.email = form.email.data
        user.username = form.username.data
        db.session.commit()
        flash('You have successfully updated your profile', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.bio.data = user.bio
        form.gender.data = user.gender
        form.email.data = user.email
        form.username.data = user.username
    return render_template('account.html', title=current_user.username + ' ' + 'Account', profile_image=profile_image,
                           form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestChangePassword
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('User does not exist', 'danger')
            return redirect(url_for('reset_password'))
        send_reset_token(user)
        flash('Your reset link has being sent to the given email', 'success')
        return redirect(url_for('users.login'))
    render_template('request_change_password.html', title='Request Reset', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid token or expired', 'warning')
        return redirect(url_for('reset_request'))
    form = ChangePasswordFormFromToken
    if form.validate_on_submit():
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        if new_password == confirm_password:
            new_hash = bcrypt.generate_password_hash(new_password)
            user.password = new_hash
            db.session.commit()
            return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form, title='Reset Password')
