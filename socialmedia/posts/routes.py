from flask_login import login_required, current_user
from flask import (flash,
                   redirect,
                   url_for,
                   render_template,
                   request,
                   Blueprint,
                   abort)
from .forms import PostCreationForm
from socialmedia.models import Post
from flask import current_app
from .utils import postsave_picture

posts = Blueprint('posts', __name__)


@posts.route('/createpost', methods=['GET', 'POST'])
@login_required
def post_create():
    form = PostCreationForm()
    if form.validate_on_submit() and form.post_image.data:
        picture_file = postsave_picture(form.post_image.data)
        post_image = picture_file
        post_title = form.post_title.data
        post_content = form.post_content.data
        create = Post(post_image=post_image, post_title=post_title, post_content=post_content, user_id=current_user.id)
        db.session.add(create)
        db.session.commit()
        flash('You have successfully created a new post', 'success')
        return redirect(url_for('main.home'))
    elif form.validate_on_submit():
        post_title = form.post_title.data
        post_content = form.post_content.data
        create = Post(post_title=post_title, post_content=post_content, user_id=current_user.id)
        db.session.add(create)
        db.session.commit()
        flash('You have successfully created a new post', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Create Post', form=form)


@posts.route('/detail/<int:user_id>')
def detail_view(user_id):
    post_detail = Post.query.get_or_404(user_id)
    return render_template('detail.html', post_detail=post_detail)


@posts.route('/detail/update/<int:post_id>', methods=['GET', 'POST'])
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


@posts.route('/detail/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You have deleted the post successfully', 'danger')
    return redirect(url_for('main.home'))
