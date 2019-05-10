from flask import Flask, render_template, url_for, flash, redirect
from forms import SignUpForm, SignInForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'c9e0b61b4e5c7f750d66180cdbf893d5'

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
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title = 'Sign Up', form=form)

@app.route("/signin", methods = ['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        # fake data to check the sign in process
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'Sign in successful for { form.email.data }!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Sign in unsuccessful! Please check your credentials!', 'danger')        
    return render_template('signin.html', title = 'Sign In', form=form)

if __name__=='__main__':
    app.run(debug=True)