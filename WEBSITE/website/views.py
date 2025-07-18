from flask_login import login_user, logout_user, login_required, current_user

# import external libraries
from flask import Blueprint, render_template, request, flash, redirect, url_for
# import database
from . import db
# import from .models user
from .models import User, Post
#set views blueprint
views = Blueprint("views", __name__)

# default/home route
@views.route("/")
@views.route("/home")
# home route function
# returns home.html
def home():
    return render_template("/home.html", user=current_user)


# blog page route
@views.route("/blog")
# user must be logged in to post
@login_required
# home route function
# returns home.html
def blog():
    posts = Post.query.all()
    return render_template("/blog.html", user=current_user, posts=posts)
# create blog post route
@views.route("/create-post", methods=['Get', 'POST'])
# user must be logged in to post
@login_required
# create blog post route function
# returns create_post.html
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        if not title:
            flash('Title cannot be empty', category='error')
        elif not content:
            flash('Blog cannot be empty', category='error')
        else:
            post = Post(title=title, content=content, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!' , category= 'success')
        return redirect(url_for('views.blog'))
   
    return render_template("/create_post.html", user=current_user)


# delete blog post route
@views.route("/delete-post/<id>")
# user must be logged in to post
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('Post does not exists', category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!' , category= 'success')
    return redirect(url_for('views.blog'))
