from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.forms import SignUpForm, SignInForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# dummy data
posts = [
    {
        'author': 'Bibishan Pandey',
        'title': 'First Blog Post',
        'content': 'First Post Content',
        'date_posted': 'May 4, 2019'
    },
    {
        'author': 'John Doe',
        'title': 'Second Blog Post',
        'content': 'Second Post Content',
        'date_posted': 'May 5, 2019'
    },
    {
        'author': 'Natsu Dragneel',
        'title': 'Third Blog Post',
        'content': 'Third Post Content',
        'date_posted': 'May 6, 2019'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash(f'Already signed in!', 'success')
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', title = 'Sign Up', form=form)

@app.route("/signin", methods = ['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        flash(f'Already signed in!', 'success')
        return redirect(url_for('home'))
    form = SignInForm()
    if form.validate_on_submit():
        # fake data to check the sign in process
        # if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Sign in successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Sign in unsuccessful! Please check your credentials!', 'danger')        
    return render_template('signin.html', title = 'Sign In', form=form)

@app.route("/signout")
def signout():
    logout_user()
    # flash(f'Sign out successful!', 'warning')
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title = 'Account')