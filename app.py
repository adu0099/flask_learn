from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Secret key for CSRF protection in forms
app.config['SECRET_KEY'] = 'e099c39d7c467f65b04a71d83a4e207b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):  # Corrected 'db.model' to 'db.Model'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)  # Corrected 'db.column' to 'db.Column'
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"  # Corrected __repr__ method


class Post(db.Model):  # Corrected 'db.model' to 'db.Model'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Corrected 'db,Column'
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Corrected 'db.Foreignkey' to 'db.ForeignKey'

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"  # Corrected __repr__ method

# Sample blog posts
posts = [
    {
        'authors': 'Ismail Hossain Adnan',
        'title': 'Blog Post 1',
        'content': 'Hello, I\'m Ismail Hossain Adnan. I\'ve recently completed my graduation from Hamdard University Bangladesh in Computer Science and Engineering.',
        'date_posted': 'June 5, 2024'
    },
    {
        'authors': 'Mashiur Rahman',
        'title': 'Blog Post 2',
        'content': 'I am barke Shimul. My girlfriend Tasfia lives in Dubai. Please help me, I am in pain.',
        'date_posted': 'June 7, 2024'
    }
]

# Route for home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

# Route for about page
@app.route("/about")
def about():
    return render_template('about.html', title="About")

# Route for register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')  # Corrected 'Craeated' to 'Created'
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
