from flask import Flask, render_template
app = Flask(__name__)

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
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)