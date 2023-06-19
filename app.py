from flask import Flask, render_template, session, redirect, flash, request
from forms import (
    LoginForm,
    RegisterForm,
    CreatePostForm,
    EditPostForm,
    ForgotPasswordForm,
    ResetPasswordForm,
)
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
from db import db
from login_required import login_required
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = "super secret key for school project"

# mail config

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)


def send_email(mailTo, title, body):
    msg = Message(title, sender=app.config.get("MAIL_USERNAME"), recipients=[mailTo])
    msg.body = body
    mail.send(msg)


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
            send_email(email, "Rejestracja", "Witaj na naszej stronie!")
            return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if session.get("email"):
        return redirect("/")

    form = ForgotPasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = request.form.get("email")
            user = db.users.find_one({"email": email})
            if user:
                send_email(
                    email,
                    "Reset hasła",
                    "Kliknij w link, aby zresetować hasło: http://localhost:5000/reset-password/"
                    + str(user.get("_id")),
                )
                flash("Wysłano email z linkiem do resetowania hasła!")
            else:
                flash("Wysłano email z linkiem do resetowania hasła!")
    return render_template("forgot-password.html", form=form)


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        id = ObjectId(token)
    except:
        return redirect("/")

    user = db.users.find_one({"_id": id})
    if not user:
        return redirect("/")

    form = ResetPasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            password = request.form.get("password")
            db.users.update_one({"_id": id}, {"$set": {"password": password}})
            flash("Hasło zostało zresetowane!")
            return redirect("/login")

    return render_template("reset-password.html", form=form)


@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("/")


@app.route("/account")
@login_required
def account():
    posts = db.posts.find({"author": session.get("email")})

    return render_template("account.html", posts=posts)


@app.route("/post/<post_id>")
def post(post_id):
    try:
        id = ObjectId(post_id)
    except:
        return redirect("/")

    post = db.posts.find_one({"_id": id})
    return render_template("post.html", post=post)


@app.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            subtitle = form.subtitle.data
            photo = form.photo.data
            text = form.text.data
            author = session.get("email")
            db.posts.insert_one(
                {
                    "title": title,
                    "text": text,
                    "subtitle": subtitle,
                    "author": author,
                    "photo": photo,
                }
            )
            return redirect("/account")
    return render_template("create-post.html", form=form)


@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    try:
        id = ObjectId(post_id)
    except:
        return redirect("/account")
    form = EditPostForm()
    post = db.posts.find_one({"_id": id})

    if request.method == "GET":
        form.title.data = post.get("title")
        form.subtitle.data = post.get("subtitle")
        form.photo.data = post.get("photo")
        form.text.data = post.get("text")

    if request.method == "POST" and session.get("email") == post.get("author"):
        if form.validate_on_submit():
            title = form.title.data
            subtitle = form.subtitle.data
            photo = form.photo.data
            text = form.text.data
            db.posts.update_one(
                {"_id": id},
                {
                    "$set": {
                        "title": title,
                        "text": text,
                        "subtitle": subtitle,
                        "photo": photo,
                    }
                },
            )
        return redirect("/account")
    elif session.get("email") != post.get("author"):
        return redirect("/")
    return render_template("edit-post.html", post=post, form=form)


@app.route("/delete-post/<post_id>")
@login_required
def delete_post(post_id):
    try:
        id = ObjectId(post_id)
    except:
        return redirect("/account")
    user = db.users.find_one({"email": session.get("email")})
    db.posts.delete_one({"_id": id, "author": user.get("email")})
    return redirect("/account")


# API
@app.route("/api/posts", methods=["GET", "POST"])
def api_posts():
    if request.method == "GET":
        limit = request.args.get("limit", 20)
        offset = request.args.get("offset", 0)
        posts = db.posts.find({}, {"_id": False}).limit(int(limit)).skip(int(offset))
        return list(posts)
    elif request.method == "POST":
        data = request.get_json()
        db.posts.insert_one(data)
        return "OK"


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
