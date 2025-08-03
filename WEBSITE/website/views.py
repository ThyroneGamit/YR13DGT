from flask_login import login_required, current_user 
# import database 
from . import db 
# import external libraries 
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify 
# import from .models user 
from .models import User, Post, Comment, Like 

# set views blueprint
views = Blueprint("views", __name__)

# default/home route
@views.route("/")
@views.route("/home")
# home route function
# returns home.html
def home():
    return render_template("home.html", user=current_user)

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        flash('Your message has been sent successfully!', category='success')
        return redirect(url_for('views.contact'))

    return render_template('contact.html', user=current_user)

# blog page route
@views.route("/blog")
# user must be logged in to post
@login_required
# home route function
# returns blog.html
def blog():
    posts = Post.query.all()
    return render_template("blog.html", user=current_user, posts=posts)

# create blog post route
@views.route("/create-post", methods=['GET', 'POST'])
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
            flash('Post created!', category='success')
        return redirect(url_for('views.blog'))
   
    return render_template("create_post.html", user=current_user)

# delete blog post route
@views.route("/delete-post/<id>")
# user must be logged in to post
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('Post does not exist', category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')
    return redirect(url_for('views.blog'))

@views.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # You can check if the email exists in your DB here.
        flash('If this email exists in our system, a password reset link has been sent.', category='info')
        return redirect(url_for('auth.login'))  # Changed to auth.login assuming you have auth blueprint

    return render_template('forgot_password.html', user=current_user)
@views.route('/teams/smc-mambas')
def team1():
    players = [
        {"name": "Seb Sanchez", "jersey": 4, "ppg": 7.4, "apg": 0.4, "rpg": 2},
        {"name": "Philip Ah Kau", "jersey": 61, "ppg": 6.2, "apg": 1, "rpg": 5},
        {"name": "Thyrone Gamit", "jersey": 23, "ppg": 5.4, "apg": 0.2, "rpg": 1},
        {"name": "Charbel Alboutros", "jersey": 77, "ppg": 4.2, "apg": 0.6, "rpg": 3},
        {"name": "Junior Siketi", "jersey": 64, "ppg": 3.5, "apg": 0.5, "rpg": 2},
        {"name": "Lucius Pang", "jersey": 31, "ppg": 3.2, "apg": 1, "rpg": 5},
        {"name": "Peter Reyes", "jersey": 37, "ppg": 3.0, "apg": 0.4, "rpg": 2},
        {"name": "Diego Trevino", "jersey": 85, "ppg": 1.2, "apg": 0.8, "rpg": 4},
        {"name": "Dane Manuyag", "jersey": 42, "ppg": 0.8, "apg": 0.4, "rpg": 2},
        {"name": "Tyrese Tupai", "jersey": 67, "ppg": 0.4, "apg": 0.4, "rpg": 2},
        {"name": "Rodrich Salazar", "jersey": 67, "ppg": 0, "apg": 0, "rpg": 0},
    ]
    return render_template('team.html', team_name="SMC Mambas", players=players, user=current_user)


@views.route('/teams/smc-vipers')
def team2():
    players = [
        {"name": "Zion Talbot", "jersey": 3, "ppg": 21.3, "apg": 5.9, "rpg": 6.7},
        {"name": "Marcus Bell", "jersey": 11, "ppg": 19.8, "apg": 4.4, "rpg": 7.2},
        {"name": "Luca Daniels", "jersey": 5, "ppg": 17.5, "apg": 6.1, "rpg": 5.1},
        {"name": "Ethan Vaka", "jersey": 9, "ppg": 16.3, "apg": 3.8, "rpg": 6.0},
        {"name": "Kaleb Hunt", "jersey": 14, "ppg": 14.7, "apg": 5.2, "rpg": 5.5},
        {"name": "Jayce Martin", "jersey": 1, "ppg": 13.1, "apg": 4.0, "rpg": 4.9},
        {"name": "Denzel Cruz", "jersey": 8, "ppg": 12.5, "apg": 3.7, "rpg": 5.3},
        {"name": "Sione Lomu", "jersey": 15, "ppg": 10.8, "apg": 2.9, "rpg": 6.8},
        {"name": "Leo Tuigamala", "jersey": 6, "ppg": 9.4, "apg": 3.1, "rpg": 4.6},
        {"name": "Andre Li", "jersey": 4, "ppg": 11.6, "apg": 3.5, "rpg": 5.0},
        {"name": "Carl Rivera", "jersey": 2, "ppg": 2.3, "apg": 0.5, "rpg": 1.1},
    ]
    return render_template('team.html', team_name="SMC Vipers", players=players, user=current_user)


@views.route('/teams/smc-pythons')
def team3():
    players = [
        {"name": "Vincent Isip", "jersey": 73, "ppg": 8.7, "apg": 2.5, "rpg": 2.9},
        {"name": "Mike Johnson", "jersey": 7, "ppg": 7.4, "apg": 2.1, "rpg": 2.2},
        {"name": "Ira Abesamis", "jersey": 26, "ppg": 3.2, "apg": 2.0, "rpg": 2.3},
        {"name": "Jayden Lee", "jersey": 15, "ppg": 6.5, "apg": 2.4, "rpg": 2.6},
        {"name": "Caleb Walker", "jersey": 23, "ppg": 5.9, "apg": 2.9, "rpg": 2.7},
        {"name": "Ethan Brown", "jersey": 3, "ppg": 4.3, "apg": 2.3, "rpg": 2.4},
        {"name": "Liam White", "jersey": 5, "ppg": 2.6, "apg": 2.0, "rpg": 2.5},
        {"name": "Noah King", "jersey": 12, "ppg": 5.1, "apg": 2.7, "rpg": 2.1},
        {"name": "Lucas Green", "jersey": 33, "ppg": 6.2, "apg": 2.8, "rpg": 2.8},
        {"name": "Isaiah Scott", "jersey": 0, "ppg": 4.9, "apg": 2.2, "rpg": 2.0},
    ]
    return render_template('team.html', team_name="SMC Pythons", players=players, user=current_user)


# blog comment route 
@views.route("/create-comment/<post_id>", methods=['POST']) 
# user must be logged in to post 
@login_required 
def create_comment(post_id): 
    text = request.form.get('text') 
    if not text: 
        flash('Comment cannot be empty', category='error') 
    else: 
        post = Post.query.filter_by(id=post_id).first()  # Added .first()
        if not post:  # Fixed logic
            flash('Post does not exist', category='error')  # Fixed spelling
        else: 
            comment = Comment(text=text, author=current_user.id, post_id=post_id) 
            db.session.add(comment) 
            db.session.commit() 
            flash("Comment added!", category='success') 
    return redirect(url_for('views.blog')) 

# delete comment post route 
@views.route("/delete-comment/<comment_id>") 
# user must be logged in to delete post 
@login_required 
def delete_comment(comment_id): 
    comment = Comment.query.filter_by(id=comment_id).first() 
    if not comment: 
        flash("Comment does not exist", category="error") 
    elif current_user.id != comment.author and current_user.id != comment.post.author: 
        flash("You do not have permission to delete this comment", category="error")  # Added category
    else: 
        db.session.delete(comment) 
        db.session.commit() 
        flash("Comment deleted!", category="success") 
    return redirect(url_for("views.blog")) 

# like comment route 
@views.route("/like-post/<post_id>", methods=['POST']) 
# user must be logged in to post 
@login_required 
def like(post_id): 
    post = Post.query.filter_by(id=post_id).first()  # Added .first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first() 
    if not post: 
        return jsonify({'error': 'Post does not exist.'}), 400  # Fixed syntax
    elif like: 
        db.session.delete(like) 
        db.session.commit() 
    else:
        like = Like(author=current_user.id, post_id=post_id) 
        db.session.add(like) 
        db.session.commit() 
    return jsonify({
        "likes": len(post.likes), 
        "liked": current_user.id in map(lambda x: x.author, post.likes)
    }) 

@views.route('/videos')
def video_footage():
    videos = [
        {
            "title": "Game Highlights: SMC Mambas vs Rivals",
            "embed_url": "https://www.youtube.com/embed/dQw4w9WgXcQ"
        },
        {
            "title": "Top 5 Dunks of the Season",
            "embed_url": "https://www.youtube.com/embed/oHg5SJYRHA0"
        }
    ]
    return render_template("videos.html", videos=videos, user=current_user)


@views.route('/store')
def store():
    products = [
        {"name": "Team Jersey", "price": 49.99, "image": "jersey.png"},
        {"name": "Basketball Shorts", "price": 22.50, "image": "shorts.png"},
        {"name": "Basketball socks", "price": 17.50, "image": "socks.png"},
        {"name": "Mouthguard", "price": 5, "image": "mouthguard.png"},
    ]
    return render_template("store.html", products=products, user=current_user)

