from flask import Blueprint, render_template,request
from socialmedia.models import Post
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=1)
    return render_template('home.html', post=post, title='Home')






