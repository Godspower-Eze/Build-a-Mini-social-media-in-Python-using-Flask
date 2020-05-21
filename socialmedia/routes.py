from socialmedia import app, db
from flask import render_template, flash, redirect
from socialmedia.models import User, Post
from socialmedia.forms import PostCreationForm, UserCreationForm


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
        return redirect('home')
    return render_template('create_post.html', title='Create Post', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserCreationForm()
    return render_template('register.html', form=form, title='Register')
