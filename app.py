from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from hash import encode_id, decode_id  
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_default_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    hashed_id = db.Column(db.String(50), unique=True, nullable=False)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(252), nullable=False)

    def __repr__(self):
        return f"<Message {self.message}>"

    def __str__(self):
        return self.message


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session.get('user_id')
    messages = Messages.query.filter_by(recipient_id=user_id).all()
    print(messages)
    return render_template('index.html', messages=messages)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("c-password")

        if not username or not password:
            return render_template("error.html", error_message="Username and password are required")
        if password != password2:
            return render_template("error.html", error_message="Passwords do not match")
        if Users.query.filter_by(username=username).first():
            return render_template("error.html", error_message="Username already exists")
        if len(username) < 3 or len(username) > 50:
            return render_template("error.html", error_message="Username must be between 3 and 50 characters")
        if len(password) < 8:
            return render_template("error.html", error_message="Password must be at least 8 characters long")

        hashed_password = generate_password_hash(password)
        new_user = Users(username=username, password=hashed_password, hashed_id="")
        db.session.add(new_user)
        db.session.commit()

        new_user.hashed_id = encode_id(new_user.id)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return render_template("error.html", error_message="Invalid credentials")

        session['user_id'] = user.id
        return redirect('/')

    return render_template('login.html')


@app.route('/user')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    
    user = Users.query.get_or_404(user_id)
    unique_link = url_for('send_message', hashed_id=user.hashed_id, _external=True)
    return render_template('profile.html', user=user, unique_link=unique_link, name=user.username)


@app.route('/message/<hashed_id>', methods=['GET', 'POST'])
def send_message(hashed_id):
    user_id = decode_id(hashed_id)
    recipient = Users.query.get_or_404(user_id)

    if request.method == 'POST':
        message_content = request.form.get("message")
        if not message_content:
            return render_template("error.html", error_message="Message cannot be empty")

        new_message = Messages(recipient_id=recipient.id, message=message_content)
        db.session.add(new_message)
        db.session.commit()

        return render_template("success.html", message="Message sent successfully!")

    return render_template('message.html', recipient=recipient, id=hashed_id)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
