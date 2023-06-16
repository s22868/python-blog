from flask import Flask, render_template, session, redirect, flash
from forms import LoginForm, RegisterForm
from db import db
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = "super secret key for school project"

@app.route('/')
def index():
    return render_template('index.html', name=session.get('email') or "")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.users.find_one({"email": email, "password": password})
        if user:
            session["email"] = email
            return redirect("/")
        else:
            flash("Niepoprawny email lub hasło!")
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', name="nazwa")

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

