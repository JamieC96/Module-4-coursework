import os
from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')

app.secret_key = 'cheese'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://module4db_0zag_user:95sfrFjkZIqTiDthVA5JzH09eJi6ZUrD@dpg-cu20mclsvqrc73f17iag-a/module4db_0zag"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Survey(db.Model):
    __tablename__ = 'survey'
    id = db.Column(db.Integer, primary_key=True)
    owns = db.Column(db.Boolean, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    name = db.Column(db.String(80), nullable=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Increased length for hashed passwords

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/basicinfo")
def basicinfo():
    return render_template("html/basicinfo.html")

@app.route("/keepingaxolotls")
def keepingaxolotls():
    return render_template("html/keepingaxolotls.html")

@app.route("/inthewild")
def inthewild():
    return render_template("html/inthewild.html")

@app.route("/gallery")
def gallery():
    return render_template("html/gallery.html")

@app.route("/survey")
def survey():
    return render_template("html/survey.html")

@app.route("/contact")
def contact():
    return render_template("html/contact.html")

@app.route('/submit', methods=['POST'])
def submit():
    try:
        owns = request.form.get('owns_axolotl') == 'on'  
        age = request.form.get('age', type=int)  
        gender = request.form.get('gender')  
        name = request.form.get('name')  
        
        new_survey = Survey(
            owns=owns,
            age=age,
            gender=gender,
            name=name
        )
        
        db.session.add(new_survey)
        db.session.commit()
        
        return redirect(url_for('survey'))

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while processing your request.", 500
    
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    if User.query.filter_by(username=username).first():
        return render_template('index.html', signup_error='Username already exists! Try another one.', login_error=None)

    hashed_password = generate_password_hash(password)  # Hash the password
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return render_template('index.html', login_error=None, signup_success='Account created successfully! Please log in.')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):  # Verify password
        session['username'] = username
        return redirect(url_for('home'))
    else:
        return render_template('index.html', login_error='Invalid credentials. Please try again.', signup_error=None)

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        user = User.query.filter_by(username=session['username']).first()
        if not user:
            return "User not found.", 404

        # Verify current password
        if not check_password_hash(user.password, current_password):
            return render_template('change_password.html', error='Current password is incorrect.')

        # Check if new passwords match
        if new_password != confirm_password:
            return render_template('change_password.html', error='New passwords do not match.')

        # Hash and update the new password
        user.password = generate_password_hash(new_password)
        db.session.commit()

        return render_template('change_password.html', success='Password changed successfully.')

    return render_template('change_password.html')

if __name__ == '__main__':
    app.run(debug=True)
