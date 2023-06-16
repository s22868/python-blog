from flask import Flask, render_template, session, redirect, flash, request
from forms import LoginForm, RegisterForm, CreatePostForm
from db import db
from bson.objectid import ObjectId

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


@app.route("/account")
def account():
    return render_template("account.html")


@app.route("/post/<post_id>")
def post(post_id):
    try:
        id = ObjectId(post_id)
    except:
        return redirect("/")

    post = db.posts.find_one({"_id": id})
    return render_template("post.html", post=post)


@app.route("/create-post", methods=["GET", "POST"])
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
def edit_post(post_id):
    try:
        id = ObjectId(post_id)
    except:
        return redirect("/account")
    form = CreatePostForm()
    post = db.posts.find_one({"_id": id})
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
