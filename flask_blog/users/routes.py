from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import (SignUpForm, SignInForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flask_blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/signup", methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash(f'Already signed in!', 'success')
        return redirect(url_for('main.home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('users.signin'))
    return render_template('signup.html', title = 'Sign Up', form=form)

@users.route("/signin", methods = ['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        flash(f'Already signed in!', 'success')
        return redirect(url_for('main.home'))
    form = SignInForm()
    if form.validate_on_submit():
        # fake data to check the sign in process
        # if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Sign in successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Sign in unsuccessful! Please check your credentials!', 'danger')        
    return render_template('signin.html', title = 'Sign In', form=form)

@users.route("/signout")
def signout():
    logout_user()
    # flash(f'Sign out successful!', 'warning')
    return redirect(url_for('main.home'))

@users.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Update successful!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'images/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        flash(f'Please sign out before!', 'warning')
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.signin'))
    return render_template('reset_request.html', title='Reset Password' , form=form)

@users.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash(f'Please sign out before!', 'warning')
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f'Token is expired!', 'danger')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Password changed!', 'success')
        return redirect(url_for('users.signin'))
    return render_template('reset_token.html', title='Reset Password' , form=form)