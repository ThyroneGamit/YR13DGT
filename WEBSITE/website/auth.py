from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint("auth", __name__)

# Register Now route - redirects to sign-up page
@auth.route("/register-now")
def register_now():
    return redirect(url_for('auth.sign_up'))

# sign-up route 
@auth.route("/sign-up", methods=['GET', 'POST']) 
def sign_up(): 
    if request.method == 'POST': 
        email = request.form.get('email') 
        username = request.form.get('username') 
        password1 = request.form.get('password1') 
        password2 = request.form.get('password2') 
        # check that the email and username are unique 
        email_exists = User.query.filter_by(email=email).first() 
        username_exists = User.query.filter_by(username=username).first() 
        # validation of password, username and email 
        if email_exists: 
            flash('Email is already in use.' , category='error') 
        elif username_exists: 
            flash('Username is already in use.' , category='error') 
        elif password1 != password2: 
            flash('Passwords do not match!' , category='error') 
        elif len(password1) < 8: 
            flash('Password is too short.' , category='error') 
        elif len(username) < 2: 
            flash('Username is too short.' , category='error') 
        elif len(email) < 4: 
            flash('Email is not valid.' , category='error') 
        else: 
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='scrypt:32768:8:1')) 
            db.session.add(new_user) 
            db.session.commit() 
            login_user(new_user, remember=True) 
            flash('Your account has been created!', category='success') 
            return redirect(url_for('views.home')) 
    return render_template("sign_up.html", user=current_user) 

# Login Route (uses username instead of email)
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get("identifier")  # could be username OR email
        password = request.form.get("password")

        # Determine if the input is an email (contains '@')
        if "@" in identifier:
            user = User.query.filter_by(email=identifier).first()
        else:
            user = User.query.filter_by(username=identifier).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password.", category="error")
        else:
            flash("Account not found.", category="error")

    return render_template("login.html", user=current_user)

# Account Page
@auth.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

# Edit Profile Route
@auth.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        # Check if username or email already exists for other users
        if new_username and new_username != current_user.username:
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user:
                flash("Username is already taken.", "error")
                return redirect(url_for('auth.edit_profile'))

        if new_email and new_email != current_user.email:
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:
                flash("Email is already in use.", "error")
                return redirect(url_for('auth.edit_profile'))

        # Update username and email
        if new_username:
            current_user.username = new_username
        if new_email:
            current_user.email = new_email

        # Handle password change
        if current_password and new_password:
            if check_password_hash(current_user.password, current_password):
                if len(new_password) >= 8:
                    current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                    flash("Password updated.", "success")
                else:
                    flash("New password must be at least 8 characters.", "error")
                    return redirect(url_for('auth.edit_profile'))
            else:
                flash("Current password is incorrect.", "error")
                return redirect(url_for('auth.edit_profile'))
        elif current_password or new_password:
            # If only one password field is filled
            flash("Please fill in both current and new password fields.", "error")
            return redirect(url_for('auth.edit_profile'))

        try:
            db.session.commit()
            flash("Profile updated.", "success")
            return redirect(url_for('auth.account'))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating your profile. Please try again.", "error")

    return render_template('edit_profile.html', user=current_user)

# Logout Route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", category="info")
    return redirect(url_for('views.home'))