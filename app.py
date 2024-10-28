from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__, template_folder='templates')
app.secret_key = 'cheese'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:O9TXTq5c31xclcOhBob1mDrPqyn4dvU5@dpg-csfsnktsvqrc739r60kg-a/axolotl_ya4x'
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
    password = db.Column(db.String(50), nullable=False)


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

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return render_template('index.html', signup_error='Username already exists! Try another one.', login_error=None)

    # Create new user and add to the database
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return render_template('index.html', login_error=None, signup_success='Account created successfully! Please log in.')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if user exists and password matches
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['username'] = username
        return redirect(url_for('home'))
    else:
        # Pass an error message if login fails
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

if __name__ == '__main__':
    app.run(debug=True)
