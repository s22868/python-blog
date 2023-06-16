from flask import Flask, render_template, session, redirect, flash, request
from forms import LoginForm, RegisterForm
from db import db

app = Flask(__name__)

app.config["SECRET_KEY"] = "super secret key for school project"


@app.route("/")
def index():
    posts = db.posts.find()
    return render_template("index.html", email=session.get("email", None), posts=posts)


@app.route("/login", methods=["GET", "POST"])
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

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.users.find_one({"email": email})
        if user:
            flash("Użytkownik o podanym adresie email już istnieje!")
        else:
            db.users.insert_one({"email": email, "password": password})
            flash("Użytkownik został zarejestrowany!")
            return redirect("/login")
        
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("/")


@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot-password.html")


# API
@app.route("/api/posts", methods=["GET", "POST"])
def api_posts():
    limit = request.args.get("limit", 20)
    offset = request.args.get("offset", 0)

    if request.method == "GET":
        posts = db.posts.find({}, {"_id": False}).limit(int(limit)).skip(int(offset))
        return list(posts)
    elif request.method == "POST":
        data = request.get_json()
        db.posts.insert_one(data)
        return "OK"


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
